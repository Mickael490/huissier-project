"""
Service d'envoi d'emails de notification.
Utilise smtplib (module standard Python) - aucune dependance externe.
"""
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings

logger = logging.getLogger(__name__)


def envoyer_email(destinataire: str, sujet: str, corps_html: str) -> bool:
    if not settings.MAIL_USERNAME or not settings.MAIL_PASSWORD:
        logger.warning("Email non envoye: MAIL_USERNAME ou MAIL_PASSWORD non configure")
        return False

    if not destinataire:
        logger.warning("Email non envoye: destinataire manquant")
        return False

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = sujet
        msg["From"] = f"Cabinet Me SAWADOGO <{settings.MAIL_FROM}>"
        msg["To"] = destinataire

        msg.attach(MIMEText(corps_html, "html", "utf-8"))

        with smtplib.SMTP(settings.MAIL_SERVER, settings.MAIL_PORT, timeout=5) as server:
            server.starttls()
            server.login(settings.MAIL_USERNAME, settings.MAIL_PASSWORD)
            server.sendmail(settings.MAIL_FROM, destinataire, msg.as_string())

        logger.info(f"Email envoye avec succes a {destinataire}")
        return True

    except Exception as e:
        logger.error(f"Erreur envoi email a {destinataire}: {e}")
        return False


def template_changement_statut(numero_dossier: str, objet: str, ancien_statut: str, nouveau_statut: str) -> str:
    labels = {
        "nouveau": "Nouveau", "en_cours": "En cours", "en_attente": "En attente",
        "termine": "Termine", "archive": "Archive", "annule": "Annule"
    }
    ancien_label = labels.get(ancien_statut, ancien_statut)
    nouveau_label = labels.get(nouveau_statut, nouveau_statut)

    return f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
      <div style="background: linear-gradient(135deg, #1e3a5f, #2d6a9f); padding: 24px; border-radius: 12px 12px 0 0;">
        <h2 style="color: white; margin: 0;">Cabinet Me SAWADOGO</h2>
        <p style="color: #cbd5e1; margin: 4px 0 0;">Huissier de Justice</p>
      </div>
      <div style="background: white; padding: 24px; border: 1px solid #e2e8f0; border-top: none; border-radius: 0 0 12px 12px;">
        <p style="color: #334155; font-size: 15px;">Bonjour,</p>
        <p style="color: #334155; font-size: 15px;">
          Le statut de votre dossier <strong>{numero_dossier}</strong> ({objet}) a ete mis a jour :
        </p>
        <div style="background: #f8fafc; border-radius: 8px; padding: 16px; margin: 16px 0; text-align: center;">
          <span style="color: #94a3b8;">{ancien_label}</span>
          <span style="margin: 0 10px; color: #1e3a5f;">&rarr;</span>
          <span style="color: #1e3a5f; font-weight: 700;">{nouveau_label}</span>
        </div>
        <p style="color: #64748b; font-size: 13px;">
          Pour plus d'informations, n'hesitez pas a contacter notre cabinet.
        </p>
        <p style="color: #94a3b8; font-size: 12px; margin-top: 24px; border-top: 1px solid #e2e8f0; padding-top: 16px;">
          Ceci est un message automatique, merci de ne pas y repondre directement.
        </p>
      </div>
    </div>
    """


def template_paiement_recu(numero_dossier: str, montant: float, type_paiement: str) -> str:
    return f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
      <div style="background: linear-gradient(135deg, #1e3a5f, #2d6a9f); padding: 24px; border-radius: 12px 12px 0 0;">
        <h2 style="color: white; margin: 0;">Cabinet Me SAWADOGO</h2>
        <p style="color: #cbd5e1; margin: 4px 0 0;">Huissier de Justice</p>
      </div>
      <div style="background: white; padding: 24px; border: 1px solid #e2e8f0; border-top: none; border-radius: 0 0 12px 12px;">
        <p style="color: #334155; font-size: 15px;">Bonjour,</p>
        <p style="color: #334155; font-size: 15px;">
          Nous accusons reception d'un paiement pour le dossier <strong>{numero_dossier}</strong> :
        </p>
        <div style="background: #f0fdf4; border-radius: 8px; padding: 16px; margin: 16px 0; text-align: center;">
          <div style="color: #16a34a; font-size: 24px; font-weight: 800;">{montant:,.0f} FCFA</div>
          <div style="color: #64748b; font-size: 13px; margin-top: 4px;">{type_paiement}</div>
        </div>
        <p style="color: #94a3b8; font-size: 12px; margin-top: 24px; border-top: 1px solid #e2e8f0; padding-top: 16px;">
          Ceci est un message automatique, merci de ne pas y repondre directement.
        </p>
      </div>
    </div>
    """


def template_nouvelle_affectation(numero_dossier: str, objet: str, priorite: str, date_limite: str, instructions: str) -> str:
    priorite_label = "Urgente" if priorite == "haute" else "Normale"
    priorite_couleur = "#ef4444" if priorite == "haute" else "#4f46e5"
    date_limite_html = f'<div style="color: #64748b; font-size: 13px; margin-top: 8px;">Date limite : <strong>{date_limite}</strong></div>' if date_limite else ""
    instructions_html = f'<p style="color: #475569; font-size: 14px; margin-top: 16px;"><strong>Instructions :</strong> {instructions}</p>' if instructions else ""

    return f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
      <div style="background: linear-gradient(135deg, #1e3a5f, #2d6a9f); padding: 24px; border-radius: 12px 12px 0 0;">
        <h2 style="color: white; margin: 0;">Cabinet Me SAWADOGO</h2>
        <p style="color: #cbd5e1; margin: 4px 0 0;">Huissier de Justice</p>
      </div>
      <div style="background: white; padding: 24px; border: 1px solid #e2e8f0; border-top: none; border-radius: 0 0 12px 12px;">
        <p style="color: #334155; font-size: 15px;">Bonjour,</p>
        <p style="color: #334155; font-size: 15px;">
          Une nouvelle mission vous a ete affectee sur le dossier <strong>{numero_dossier}</strong> ({objet}) :
        </p>
        <div style="background: #f8fafc; border-radius: 8px; padding: 16px; margin: 16px 0;">
          <span style="background: {priorite_couleur}; color: white; font-size: 12px; font-weight: 700; padding: 4px 10px; border-radius: 20px;">{priorite_label}</span>
          {date_limite_html}
        </div>
        {instructions_html}
        <p style="color: #94a3b8; font-size: 12px; margin-top: 24px; border-top: 1px solid #e2e8f0; padding-top: 16px;">
          Ceci est un message automatique, merci de ne pas y repondre directement.
        </p>
      </div>
    </div>
    """


def template_nouveau_rendezvous(titre: str, date_debut: str, lieu: str, type_rdv: str) -> str:
    return f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
      <div style="background: linear-gradient(135deg, #1e3a5f, #2d6a9f); padding: 24px; border-radius: 12px 12px 0 0;">
        <h2 style="color: white; margin: 0;">Cabinet Me SAWADOGO</h2>
        <p style="color: #cbd5e1; margin: 4px 0 0;">Huissier de Justice</p>
      </div>
      <div style="background: white; padding: 24px; border: 1px solid #e2e8f0; border-top: none; border-radius: 0 0 12px 12px;">
        <p style="color: #334155; font-size: 15px;">Bonjour,</p>
        <p style="color: #334155; font-size: 15px;">
          Un rendez-vous a ete planifie avec notre cabinet :
        </p>
        <div style="background: #f8fafc; border-radius: 8px; padding: 16px; margin: 16px 0;">
          <div style="color: #1e3a5f; font-weight: 700; font-size: 16px;">{titre}</div>
          <div style="color: #64748b; font-size: 13px; margin-top: 6px;">{date_debut}</div>
          <div style="color: #64748b; font-size: 13px; margin-top: 2px;">{lieu or "Lieu a confirmer"}</div>
        </div>
        <p style="color: #94a3b8; font-size: 12px; margin-top: 24px; border-top: 1px solid #e2e8f0; padding-top: 16px;">
          Ceci est un message automatique, merci de ne pas y repondre directement.
        </p>
      </div>
    </div>
    """


def template_rappel_echeance(titre: str, date_debut: str, lieu: str) -> str:
    return f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
      <div style="background: linear-gradient(135deg, #f97316, #ea580c); padding: 24px; border-radius: 12px 12px 0 0;">
        <h2 style="color: white; margin: 0;">Rappel — Cabinet Me SAWADOGO</h2>
        <p style="color: #fed7aa; margin: 4px 0 0;">Huissier de Justice</p>
      </div>
      <div style="background: white; padding: 24px; border: 1px solid #e2e8f0; border-top: none; border-radius: 0 0 12px 12px;">
        <p style="color: #334155; font-size: 15px;">Bonjour,</p>
        <p style="color: #334155; font-size: 15px;">
          Rappel : vous avez un rendez-vous prevu prochainement :
        </p>
        <div style="background: #fff7ed; border-radius: 8px; padding: 16px; margin: 16px 0;">
          <div style="color: #9a3412; font-weight: 700; font-size: 16px;">{titre}</div>
          <div style="color: #78350f; font-size: 13px; margin-top: 6px;">{date_debut}</div>
          <div style="color: #78350f; font-size: 13px; margin-top: 2px;">{lieu or "Lieu a confirmer"}</div>
        </div>
        <p style="color: #94a3b8; font-size: 12px; margin-top: 24px; border-top: 1px solid #e2e8f0; padding-top: 16px;">
          Ceci est un message automatique, merci de ne pas y repondre directement.
        </p>
      </div>
    </div>
    """
