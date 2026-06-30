# -*- coding: utf-8 -*-
"""Génération des diagrammes (UML, Merise, architecture, Gantt, mockups)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch, Ellipse, Circle
import os

IMG = os.path.join(os.path.dirname(__file__), "img")
os.makedirs(IMG, exist_ok=True)

NAVY = "#1e3a5f"
INDIGO = "#4f46e5"
GREEN = "#10b981"
ORANGE = "#f97316"
CYAN = "#06b6d4"
PURPLE = "#8b5cf6"
GREY = "#64748b"
LIGHT = "#eef2ff"


def _box(ax, x, y, w, h, text, fc="white", ec=NAVY, fs=9, bold=False, tc="#1e293b", radius=0.02):
    p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0.01,rounding_size={radius}",
                       linewidth=1.4, edgecolor=ec, facecolor=fc, zorder=2)
    ax.add_patch(p)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs,
            weight="bold" if bold else "normal", color=tc, zorder=3, wrap=True)


def _arrow(ax, x1, y1, x2, y2, style="-|>", color=GREY, ls="-", lw=1.3):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=14,
                        color=color, lw=lw, linestyle=ls, zorder=1)
    ax.add_patch(a)


def _save(fig, name):
    fig.savefig(os.path.join(IMG, name), dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)


# ---------------------------------------------------------------- Organigramme
def organigramme():
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.set_xlim(0, 10); ax.set_ylim(0, 8); ax.axis("off")
    _box(ax, 3.5, 6.8, 3, 0.9, "Huissier de Justice\n(Titulaire du cabinet)", fc=NAVY, tc="white", bold=True, fs=10)
    roles = [
        (0.3, 4.8, "Clerc principal\n(Rédaction des actes)", INDIGO),
        (3.6, 4.8, "Clerc significateur\n(Signification / exécution)", INDIGO),
        (6.9, 4.8, "Secrétaire\n(Accueil, courrier)", ORANGE),
    ]
    for x, y, t, c in roles:
        _box(ax, x, y, 2.8, 0.9, t, fc="white", ec=c, tc=c, bold=True, fs=9)
        _arrow(ax, 5, 6.8, x + 1.4, 5.7, color=GREY)
    bas = [
        (0.3, 2.8, "Assistant juridique\n(Suivi des dossiers)", GREEN),
        (3.6, 2.8, "Comptable\n(Paiements, provisions)", GREEN),
        (6.9, 2.8, "Agent de saisie\n(Archivage)", GREEN),
    ]
    for x, y, t, c in bas:
        _box(ax, x, y, 2.8, 0.9, t, fc="white", ec=c, tc=c, fs=9)
    _arrow(ax, 1.7, 4.8, 1.7, 3.7); _arrow(ax, 5, 4.8, 5, 3.7); _arrow(ax, 8.3, 4.8, 8.3, 3.7)
    ax.set_title("Figure : Organigramme type d'un cabinet d'huissier de justice", fontsize=10, color=NAVY, weight="bold")
    _save(fig, "organigramme.png")


# ---------------------------------------------------------------- Architecture 3-tiers
def architecture():
    fig, ax = plt.subplots(figsize=(9.5, 6.5))
    ax.set_xlim(0, 12); ax.set_ylim(0, 9); ax.axis("off")
    # Couche présentation
    _box(ax, 0.5, 6.6, 11, 1.9, "", fc=LIGHT, ec=INDIGO)
    ax.text(1, 8.2, "COUCHE PRÉSENTATION (Client)", fontsize=10, color=INDIGO, weight="bold")
    for i, (t) in enumerate(["Navigateur\nweb", "Angular 17\n(SPA)", "PrimeNG\n+ Chart.js", "Garde de\nrôles (RBAC)"]):
        _box(ax, 1 + i * 2.7, 6.85, 2.3, 1.0, t, fc="white", ec=INDIGO, tc=INDIGO, fs=9)
    # Couche métier
    _box(ax, 0.5, 3.6, 11, 1.9, "", fc="#ecfdf5", ec=GREEN)
    ax.text(1, 5.2, "COUCHE MÉTIER / SERVICE (Serveur d'application)", fontsize=10, color=GREEN, weight="bold")
    for i, t in enumerate(["API REST\nFastAPI", "Services\nmétier", "Authentif.\nJWT", "Tâches\nasynchrones\n(Celery)"]):
        _box(ax, 1 + i * 2.7, 3.85, 2.3, 1.0, t, fc="white", ec=GREEN, tc=GREEN, fs=9)
    # Couche données
    _box(ax, 0.5, 0.6, 11, 1.9, "", fc="#fff7ed", ec=ORANGE)
    ax.text(1, 2.2, "COUCHE DONNÉES (Persistance)", fontsize=10, color=ORANGE, weight="bold")
    for i, t in enumerate(["ORM\nSQLAlchemy", "PostgreSQL\n(dossier_db)", "Stockage\nfichiers", "Migrations\nAlembic"]):
        _box(ax, 1 + i * 2.7, 0.85, 2.3, 1.0, t, fc="white", ec=ORANGE, tc=ORANGE, fs=9)
    _arrow(ax, 6, 6.6, 6, 5.5, style="<|-|>", color=NAVY); ax.text(6.2, 6.0, "HTTPS / JSON", fontsize=8, color=NAVY)
    _arrow(ax, 6, 3.6, 6, 2.5, style="<|-|>", color=NAVY); ax.text(6.2, 3.0, "SQL", fontsize=8, color=NAVY)
    ax.set_title("Figure : Architecture logique 3-tiers de l'application", fontsize=10, color=NAVY, weight="bold")
    _save(fig, "architecture.png")


# ---------------------------------------------------------------- Cas d'utilisation
def use_case():
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_xlim(0, 12); ax.set_ylim(0, 11); ax.axis("off")
    # système
    ax.add_patch(Rectangle((3, 0.5), 6, 10, fill=False, edgecolor=NAVY, lw=1.6))
    ax.text(6, 10.1, "Application de gestion du cabinet d'huissier", ha="center", fontsize=10, color=NAVY, weight="bold")

    def actor(x, y, name):
        ax.add_patch(Circle((x, y + 0.45), 0.18, fill=False, ec="black", lw=1.4))
        ax.plot([x, x], [y + 0.27, y - 0.15], "k-", lw=1.4)
        ax.plot([x - 0.25, x + 0.25], [y + 0.1, y + 0.1], "k-", lw=1.4)
        ax.plot([x, x - 0.22], [y - 0.15, y - 0.5], "k-", lw=1.4)
        ax.plot([x, x + 0.22], [y - 0.15, y - 0.5], "k-", lw=1.4)
        ax.text(x, y - 0.8, name, ha="center", fontsize=8.5, weight="bold")

    actor(1.2, 8.5, "Administrateur")
    actor(1.2, 5.2, "Huissier")
    actor(1.2, 2.2, "Clerc /\nSecrétaire")

    ucs = [
        (6, 9.4, "S'authentifier"),
        (5, 8.4, "Gérer les utilisateurs\net les rôles"),
        (7, 7.5, "Gérer les dossiers"),
        (5, 6.6, "Gérer les clients\net les parties"),
        (7, 5.7, "Rédiger les actes"),
        (5, 4.8, "Planifier les\nactivités (agenda)"),
        (7, 3.9, "Suivre les paiements"),
        (5, 3.0, "Gérer les documents\net archives"),
        (7, 2.1, "Consulter le\ntableau de bord"),
        (5, 1.2, "Consulter les\njournaux d'audit"),
    ]
    pos = {}
    for x, y, t in ucs:
        ax.add_patch(Ellipse((x, y), 2.2, 0.7, fill=True, fc=LIGHT, ec=INDIGO, lw=1.2))
        ax.text(x, y, t, ha="center", va="center", fontsize=7.5, color=NAVY)
        pos[t] = (x, y)
    # liaisons
    for t in ["S'authentifier", "Gérer les utilisateurs\net les rôles", "Consulter les\njournaux d'audit"]:
        _arrow(ax, 1.55, 8.5, pos[t][0] - 1.1, pos[t][1], style="-", color=GREY)
    for t in ["Gérer les dossiers", "Rédiger les actes", "Suivre les paiements", "Consulter le\ntableau de bord"]:
        _arrow(ax, 1.55, 5.2, pos[t][0] - 1.1, pos[t][1], style="-", color=GREY)
    for t in ["Gérer les clients\net les parties", "Planifier les\nactivités (agenda)", "Gérer les documents\net archives"]:
        _arrow(ax, 1.55, 2.2, pos[t][0] - 1.1, pos[t][1], style="-", color=GREY)
    ax.set_title("Figure : Diagramme de cas d'utilisation global", fontsize=10, color=NAVY, weight="bold")
    _save(fig, "usecase.png")


# ---------------------------------------------------------------- Diagramme de classes
def class_diagram():
    fig, ax = plt.subplots(figsize=(11, 8.5))
    ax.set_xlim(0, 14); ax.set_ylim(0, 11); ax.axis("off")

    def cls(x, y, name, attrs, w=2.7):
        h_title = 0.5
        h_attr = 0.28 * len(attrs) + 0.2
        ax.add_patch(Rectangle((x, y), w, h_title, fc=NAVY, ec=NAVY))
        ax.text(x + w / 2, y + h_title / 2, name, ha="center", va="center", color="white", weight="bold", fontsize=8.5)
        ax.add_patch(Rectangle((x, y - h_attr), w, h_attr, fc="white", ec=NAVY))
        for i, a in enumerate(attrs):
            ax.text(x + 0.1, y - 0.25 - i * 0.28, a, ha="left", va="center", fontsize=6.8, color="#1e293b")
        return (x, y, w, h_attr)

    cls(5.5, 10.4, "Cabinet", ["- id : int", "- nom", "- adresse", "- telephone"])
    cls(0.4, 8.2, "Utilisateur", ["- id", "- nom, prenom", "- email", "- mot_de_passe", "- role : Role"])
    cls(5.5, 8.2, "Dossier", ["- id", "- numero_dossier", "- objet", "- type_dossier", "- statut", "- date_creation"])
    cls(10.3, 8.2, "Client", ["- id", "- nom / raison", "- type_client", "- telephone", "- email"])
    cls(0.4, 5.0, "Acte", ["- id", "- type_acte", "- date_acte", "- resultat", "- observations"])
    cls(5.5, 5.0, "Partie", ["- id", "- nom", "- role_partie", "- adresse"])
    cls(10.3, 5.0, "Paiement", ["- id", "- montant", "- type_paiement", "- mode_paiement", "- date_paiement"])
    cls(0.4, 2.2, "Document", ["- id", "- nom_fichier", "- type", "- chemin", "- date_ajout"])
    cls(5.5, 2.2, "Agenda", ["- id", "- titre", "- type_rdv", "- date_debut", "- date_fin", "- lieu"])
    cls(10.3, 2.2, "AuditLog", ["- id", "- action", "- entity_type", "- description", "- date_action"])

    _arrow(ax, 6.8, 9.9, 6.8, 8.5, style="-|>", color=NAVY)            # Cabinet-Dossier
    _arrow(ax, 3.1, 7.6, 5.5, 7.6, style="-|>", color=GREY)            # User-Dossier
    _arrow(ax, 10.3, 7.6, 8.2, 7.6, style="-|>", color=GREY)           # Client-Dossier
    _arrow(ax, 6.0, 6.6, 3.1, 4.7, style="-|>", color=GREY)            # Dossier-Acte
    _arrow(ax, 6.8, 6.6, 6.8, 5.5, style="-|>", color=GREY)            # Dossier-Partie
    _arrow(ax, 7.5, 6.6, 11.0, 5.5, style="-|>", color=GREY)           # Dossier-Paiement
    _arrow(ax, 6.0, 6.6, 2.0, 2.7, style="-|>", color=GREY, ls="--")   # Dossier-Document
    _arrow(ax, 6.8, 6.6, 6.8, 2.7, style="-|>", color=GREY, ls="--")   # Dossier-Agenda
    ax.text(13.0, 9.0, "1\n\n*", fontsize=7, color=NAVY)
    ax.set_title("Figure : Diagramme de classes (vue simplifiée du domaine)", fontsize=10, color=NAVY, weight="bold")
    _save(fig, "classes.png")


# ---------------------------------------------------------------- MCD Merise
def mcd():
    fig, ax = plt.subplots(figsize=(11, 8))
    ax.set_xlim(0, 14); ax.set_ylim(0, 10); ax.axis("off")

    def entite(x, y, name, attrs, w=2.6):
        h = 0.45 + 0.26 * len(attrs)
        ax.add_patch(Rectangle((x, y - h), w, h, fc="white", ec=NAVY, lw=1.4))
        ax.add_patch(Rectangle((x, y - 0.45), w, 0.45, fc=INDIGO, ec=NAVY, lw=1.4))
        ax.text(x + w / 2, y - 0.22, name, ha="center", va="center", color="white", weight="bold", fontsize=8.5)
        for i, a in enumerate(attrs):
            ax.text(x + 0.1, y - 0.7 - i * 0.26, a, ha="left", fontsize=6.8)
        return (x + w / 2, y - h / 2, w, h)

    def assoc(x, y, name, card=""):
        ax.add_patch(Ellipse((x, y), 1.5, 0.6, fc="#fef3c7", ec=ORANGE, lw=1.3))
        ax.text(x, y, name, ha="center", va="center", fontsize=7, color="#92400e")

    c = entite(5.5, 9.7, "CABINET", ["# id_cabinet", "nom", "adresse"])
    u = entite(0.3, 7.2, "UTILISATEUR", ["# id_user", "nom", "email", "role"])
    d = entite(5.5, 6.6, "DOSSIER", ["# id_dossier", "numero", "objet", "statut", "date_creation"])
    cl = entite(10.6, 7.2, "CLIENT", ["# id_client", "nom", "type_client", "tel"])
    a = entite(0.3, 3.2, "ACTE", ["# id_acte", "type_acte", "date_acte", "resultat"])
    p = entite(5.5, 2.6, "PARTIE", ["# id_partie", "nom", "role_partie"])
    pa = entite(10.6, 3.2, "PAIEMENT", ["# id_paiement", "montant", "mode", "date"])

    assoc(5.6, 8.4, "appartenir"); _arrow(ax, 5.6, 9.0, 5.6, 8.7, style="-", color=ORANGE); _arrow(ax, 5.6, 8.1, 5.6, 7.2, style="-", color=ORANGE)
    ax.text(5.7, 8.85, "1,1", fontsize=6.5); ax.text(5.7, 7.4, "1,n", fontsize=6.5)
    assoc(3.0, 7.0, "gérer"); _arrow(ax, 1.6, 7.0, 2.3, 7.0, style="-", color=ORANGE); _arrow(ax, 3.7, 6.9, 5.5, 6.7, style="-", color=ORANGE)
    assoc(8.4, 7.0, "concerner"); _arrow(ax, 7.0, 6.8, 7.7, 6.95, style="-", color=ORANGE); _arrow(ax, 9.1, 7.0, 10.6, 7.1, style="-", color=ORANGE)
    assoc(3.0, 4.6, "contenir"); _arrow(ax, 5.0, 5.6, 3.6, 4.9, style="-", color=ORANGE); _arrow(ax, 2.5, 4.3, 1.6, 3.5, style="-", color=ORANGE)
    assoc(5.6, 4.6, "impliquer"); _arrow(ax, 5.6, 5.6, 5.6, 4.9, style="-", color=ORANGE); _arrow(ax, 5.6, 4.3, 5.6, 3.2, style="-", color=ORANGE)
    assoc(8.4, 4.6, "régler"); _arrow(ax, 6.5, 5.6, 7.8, 4.9, style="-", color=ORANGE); _arrow(ax, 9.0, 4.3, 10.2, 3.6, style="-", color=ORANGE)
    ax.set_title("Figure : Modèle Conceptuel de Données (MCD - Merise)", fontsize=10, color=NAVY, weight="bold")
    _save(fig, "mcd.png")


# ---------------------------------------------------------------- Séquence (auth)
def sequence_auth():
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.set_xlim(0, 12); ax.set_ylim(0, 10); ax.axis("off")
    lignes = [("Utilisateur", 1.5), ("Interface\nAngular", 4), ("API FastAPI", 7), ("Service Auth\n+ JWT", 9.3), ("BD\nPostgreSQL", 11)]
    for name, x in lignes:
        _box(ax, x - 0.9, 9.0, 1.8, 0.7, name, fc=NAVY, tc="white", fs=8, bold=True)
        ax.plot([x, x], [0.4, 9.0], color=GREY, ls="--", lw=1)
    steps = [
        (1.5, 4, "1. Saisie email + mot de passe", 8.4),
        (4, 7, "2. POST /auth/login", 7.7),
        (7, 9.3, "3. Vérifier identifiants", 7.0),
        (9.3, 11, "4. SELECT utilisateur", 6.3),
        (11, 9.3, "5. Données utilisateur", 5.6),
        (9.3, 7, "6. Générer token JWT", 4.9),
        (7, 4, "7. 200 OK + token + rôle", 4.2),
        (4, 1.5, "8. Stockage token + redirection", 3.5),
    ]
    for x1, x2, label, y in steps:
        rev = x2 < x1
        _arrow(ax, x1, y, x2, y, style="-|>", color=INDIGO)
        ax.text((x1 + x2) / 2, y + 0.12, label, ha="center", fontsize=7, color="#1e293b")
    ax.set_title("Figure : Diagramme de séquence — Authentification", fontsize=10, color=NAVY, weight="bold")
    _save(fig, "sequence_auth.png")


# ---------------------------------------------------------------- Séquence (création dossier)
def sequence_dossier():
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.set_xlim(0, 12); ax.set_ylim(0, 10); ax.axis("off")
    lignes = [("Clerc", 1.5), ("Interface\nAngular", 4), ("API FastAPI", 7), ("Service\nDossier", 9.3), ("BD + Audit", 11)]
    for name, x in lignes:
        _box(ax, x - 0.9, 9.0, 1.8, 0.7, name, fc=GREEN, tc="white", fs=8, bold=True)
        ax.plot([x, x], [0.4, 9.0], color=GREY, ls="--", lw=1)
    steps = [
        (1.5, 4, "1. Remplir formulaire dossier", 8.4),
        (4, 7, "2. POST /dossiers (JWT)", 7.7),
        (7, 9.3, "3. Valider données (Pydantic)", 7.0),
        (9.3, 11, "4. INSERT dossier + log audit", 6.3),
        (11, 9.3, "5. Confirmation", 5.6),
        (9.3, 7, "6. Objet Dossier créé", 4.9),
        (7, 4, "7. 201 Created", 4.2),
        (4, 1.5, "8. Notification + rafraîchir table", 3.5),
    ]
    for x1, x2, label, y in steps:
        _arrow(ax, x1, y, x2, y, style="-|>", color=GREEN)
        ax.text((x1 + x2) / 2, y + 0.12, label, ha="center", fontsize=7, color="#1e293b")
    ax.set_title("Figure : Diagramme de séquence — Création d'un dossier", fontsize=10, color=NAVY, weight="bold")
    _save(fig, "sequence_dossier.png")


# ---------------------------------------------------------------- Activité
def activite():
    fig, ax = plt.subplots(figsize=(7, 9))
    ax.set_xlim(0, 8); ax.set_ylim(0, 12); ax.axis("off")
    ax.add_patch(Circle((4, 11.4), 0.22, fc="black"))
    flow = [
        (4, 10.2, "Se connecter à l'application", INDIGO, "box"),
        (4, 9.2, "Authentification valide ?", ORANGE, "dec"),
        (4, 7.9, "Accéder au tableau de bord", INDIGO, "box"),
        (4, 6.9, "Créer / ouvrir un dossier", INDIGO, "box"),
        (4, 5.9, "Saisir clients, parties, actes", INDIGO, "box"),
        (4, 4.9, "Planifier RDV / enregistrer paiement", INDIGO, "box"),
        (4, 3.9, "Joindre documents", INDIGO, "box"),
        (4, 2.9, "Dossier clôturé ?", ORANGE, "dec"),
        (4, 1.6, "Archiver le dossier", GREEN, "box"),
    ]
    prev = (4, 11.18)
    for x, y, t, c, shape in flow:
        if shape == "box":
            _box(ax, x - 1.6, y - 0.35, 3.2, 0.7, t, fc="white", ec=c, tc=c, fs=8)
            top = (x, y + 0.35)
        else:
            ax.add_patch(plt.Polygon([(x, y + 0.45), (x + 1.5, y), (x, y - 0.45), (x - 1.5, y)], fc="#fef3c7", ec=c))
            ax.text(x, y, t, ha="center", va="center", fontsize=7.5, color="#92400e")
            top = (x, y + 0.45)
        _arrow(ax, prev[0], prev[1], top[0], top[1], style="-|>", color=GREY)
        prev = (x, y - (0.45 if shape == "dec" else 0.35))
    ax.text(5.7, 9.2, "non → retour login", fontsize=7, color="#ef4444")
    ax.text(5.7, 2.9, "non → suivi", fontsize=7, color="#ef4444")
    ax.add_patch(Circle((4, 0.7), 0.26, fc="white", ec="black", lw=2))
    ax.add_patch(Circle((4, 0.7), 0.14, fc="black"))
    _arrow(ax, 4, 1.25, 4, 0.96, style="-|>", color=GREY)
    ax.set_title("Figure : Diagramme d'activité — Cycle de vie d'un dossier", fontsize=9.5, color=NAVY, weight="bold")
    _save(fig, "activite.png")


# ---------------------------------------------------------------- Déploiement
def deploiement():
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, 12); ax.set_ylim(0, 8); ax.axis("off")
    _box(ax, 0.5, 2.5, 3, 3, "", fc=LIGHT, ec=INDIGO)
    ax.text(2, 5.2, "Poste client", fontsize=9, color=INDIGO, weight="bold", ha="center")
    _box(ax, 0.9, 3.0, 2.2, 1.4, "Navigateur\nweb\n(Angular SPA)", fc="white", ec=INDIGO, tc=INDIGO, fs=8)
    _box(ax, 4.5, 1.0, 4, 6, "", fc="#ecfdf5", ec=GREEN)
    ax.text(6.5, 6.7, "Serveur d'application", fontsize=9, color=GREEN, weight="bold", ha="center")
    _box(ax, 4.9, 4.8, 3.2, 1.1, "Serveur web (Uvicorn)\n+ API FastAPI", fc="white", ec=GREEN, tc=GREEN, fs=8)
    _box(ax, 4.9, 3.2, 3.2, 1.1, "Worker Celery\n(tâches asynchrones)", fc="white", ec=GREEN, tc=GREEN, fs=8)
    _box(ax, 4.9, 1.6, 3.2, 1.1, "Broker de messages\n(RabbitMQ)", fc="white", ec=GREEN, tc=GREEN, fs=8)
    _box(ax, 9.2, 2.5, 2.5, 3, "", fc="#fff7ed", ec=ORANGE)
    ax.text(10.45, 5.2, "Serveur BD", fontsize=9, color=ORANGE, weight="bold", ha="center")
    _box(ax, 9.5, 3.0, 1.9, 1.4, "SGBD\nPostgreSQL", fc="white", ec=ORANGE, tc=ORANGE, fs=8)
    _arrow(ax, 3.5, 3.7, 4.9, 5.3, style="<|-|>", color=NAVY); ax.text(3.7, 4.7, "HTTPS", fontsize=7, color=NAVY)
    _arrow(ax, 8.1, 5.3, 9.5, 3.9, style="<|-|>", color=NAVY); ax.text(8.3, 4.7, "TCP/5432", fontsize=7, color=NAVY)
    ax.set_title("Figure : Diagramme de déploiement", fontsize=10, color=NAVY, weight="bold")
    _save(fig, "deploiement.png")


# ---------------------------------------------------------------- Gantt
def gantt():
    fig, ax = plt.subplots(figsize=(10, 5.5))
    taches = [
        ("Prise de contact & cadrage", 0, 1, NAVY),
        ("Étude de l'existant", 1, 1.5, INDIGO),
        ("Spécification des besoins", 2, 1.5, INDIGO),
        ("Analyse & conception (UML/Merise)", 3, 2, GREEN),
        ("Conception base de données", 4.5, 1.5, GREEN),
        ("Développement backend (FastAPI)", 5.5, 3, ORANGE),
        ("Développement frontend (Angular)", 7, 3, ORANGE),
        ("Intégration & tests", 9.5, 1.5, PURPLE),
        ("Sécurité & RBAC", 10, 1.5, PURPLE),
        ("Rédaction du rapport", 10.5, 2, CYAN),
    ]
    for i, (t, start, dur, c) in enumerate(taches):
        ax.barh(len(taches) - i, dur, left=start, color=c, edgecolor="white", height=0.6)
        ax.text(start + dur + 0.1, len(taches) - i, t, va="center", fontsize=8)
    ax.set_yticks([]); ax.set_xlabel("Semaines", fontsize=9)
    ax.set_xlim(0, 16); ax.set_xticks(range(0, 13))
    ax.set_title("Figure : Diagramme de Gantt — Planning de réalisation du stage", fontsize=10, color=NAVY, weight="bold")
    ax.grid(axis="x", ls=":", alpha=0.4)
    _save(fig, "gantt.png")


# ---------------------------------------------------------------- Mockups interfaces
def mockup_login():
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.set_xlim(0, 10); ax.set_ylim(0, 7); ax.axis("off")
    ax.add_patch(Rectangle((0, 0), 10, 7, fc="#1e3a5f"))
    _box(ax, 3, 1.5, 4, 4, "", fc="white", radius=0.05)
    ax.text(5, 4.9, "⚖  Cabinet Me SAWADOGO", ha="center", fontsize=11, color=NAVY, weight="bold")
    ax.text(5, 4.5, "Connexion sécurisée", ha="center", fontsize=8, color=GREY)
    _box(ax, 3.4, 3.6, 3.2, 0.5, "Email", fc="#f8fafc", ec="#cbd5e1", fs=8, tc=GREY)
    _box(ax, 3.4, 2.9, 3.2, 0.5, "Mot de passe", fc="#f8fafc", ec="#cbd5e1", fs=8, tc=GREY)
    _box(ax, 3.4, 2.1, 3.2, 0.55, "SE CONNECTER", fc=INDIGO, tc="white", fs=9, bold=True)
    ax.set_title("Figure : Maquette — Écran de connexion", fontsize=10, color=NAVY, weight="bold")
    _save(fig, "mockup_login.png")


def mockup_dashboard():
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, 14); ax.set_ylim(0, 9); ax.axis("off")
    ax.add_patch(Rectangle((0, 0), 2.4, 9, fc=NAVY))
    ax.text(1.2, 8.4, "MENU", ha="center", color="white", fontsize=8, weight="bold")
    for i, m in enumerate(["Tableau de bord", "Dossiers", "Clients", "Actes", "Paiements", "Agenda", "Archives", "Audit"]):
        ax.text(0.2, 7.7 - i * 0.55, "• " + m, color="white", fontsize=7.5)
    ax.add_patch(Rectangle((2.6, 7.4, ), 11.2, 1.4, fc="#2d6a9f"))
    ax.text(2.9, 8.1, "Bonjour, Utilisateur 👋", color="white", fontsize=10, weight="bold")
    kpis = [("Dossiers", "128", INDIGO), ("Encaissements", "2 450 000", GREEN), ("Clients", "76", ORANGE), ("RDV", "5", CYAN)]
    for i, (t, v, c) in enumerate(kpis):
        _box(ax, 2.9 + i * 2.75, 5.6, 2.5, 1.4, "", fc="white", ec=c)
        ax.text(3.05 + i * 2.75, 6.7, t, fontsize=7.5, color=GREY)
        ax.text(3.05 + i * 2.75, 6.1, v, fontsize=12, color=c, weight="bold")
    _box(ax, 2.9, 0.6, 5.2, 4.6, "", fc="white", ec="#e2e8f0")
    ax.text(3.2, 4.8, "Répartition par type", fontsize=8, color=NAVY, weight="bold")
    ax.add_patch(Circle((5.5, 2.6), 1.4, fc=LIGHT, ec=INDIGO))
    ax.add_patch(Circle((5.5, 2.6), 0.7, fc="white"))
    _box(ax, 8.4, 0.6, 5.3, 4.6, "", fc="white", ec="#e2e8f0")
    ax.text(8.7, 4.8, "Dossiers par statut", fontsize=8, color=NAVY, weight="bold")
    for i, h in enumerate([2.5, 3.5, 1.8, 3.0, 2.2]):
        ax.add_patch(Rectangle((9.0 + i * 0.9, 1.0), 0.6, h, fc=[INDIGO, GREEN, ORANGE, PURPLE, CYAN][i]))
    ax.set_title("Figure : Maquette — Tableau de bord", fontsize=10, color=NAVY, weight="bold")
    _save(fig, "mockup_dashboard.png")


if __name__ == "__main__":
    organigramme(); architecture(); use_case(); class_diagram(); mcd()
    sequence_auth(); sequence_dossier(); activite(); deploiement(); gantt()
    mockup_login(); mockup_dashboard()
    print("Diagrammes générés dans", IMG)
