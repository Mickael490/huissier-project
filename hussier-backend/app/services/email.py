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
