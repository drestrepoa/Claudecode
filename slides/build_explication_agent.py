#!/usr/bin/env python3
"""L'agent de messagerie expliqué, avec captures de l'application en français, et quatre exercices de quinze minutes.

  SHOTS=<dossier des captures> python3 slides/build_explication_agent.py   -> slides/agent-messagerie-explication.pptx

Les captures viennent d'un passage automatisé sur la page construite (data/hr, mode FR) ; sans dossier SHOTS, les
emplacements d'image restent vides mais le deck se construit. Format maison via build_challenge_deck.py ; le schéma
progressif vient de build_exercice_15min.py.
"""
import os
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from build_challenge_deck import (  # noqa: E402
    BLACK, GOLD, GREY, KIND, LIGHT, NAVY, NAVY_LINE, SITE, arrow, callout, card, chip, fresh, layout, legend, node, notes, number, textbox, title,
)
from build_exercice_15min import flow  # noqa: E402
from pptx.dml.color import RGBColor  # noqa: E402
from pptx.enum.shapes import MSO_SHAPE  # noqa: E402
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN  # noqa: E402
from pptx.util import Inches, Pt  # noqa: E402

KIND["skill"] = ("EEEAF9", "5E48B8", True)
SHOTS = Path(os.environ.get("SHOTS", "")) if os.environ.get("SHOTS") else None


def picture(s, name, x, y, w=None, h=None):
    """Place a screenshot, fitted inside w × h (inches), top-left at x, y. Returns the height used."""
    p = SHOTS / f"{name}.png" if SHOTS else None
    if not p or not p.exists():
        r = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w or 4), Inches(h or 2.5)); r.fill.solid(); r.fill.fore_color.rgb = RGBColor.from_string(LIGHT); r.line.fill.background()
        textbox(s, x + 0.2, y + 0.2, (w or 4) - 0.4, 0.4, [(f"capture : {name}", {"size": 10, "color": GREY})]); return h or 2.5
    from PIL import Image
    iw, ih = Image.open(p).size; ratio = ih / iw
    if w and h:
        if w * ratio <= h: ww, hh = w, w * ratio
        else: ww, hh = h / ratio, h
    elif w: ww, hh = w, w * ratio
    else: ww, hh = h / ratio, h
    pic = s.shapes.add_picture(str(p), Inches(x), Inches(y), width=Inches(ww), height=Inches(hh))
    pic.line.color.rgb = RGBColor.from_string("D9DCE3"); pic.line.width = Pt(0.75)
    return hh


def numbered(s, items, x, y, w, size=11.5):
    for i, (lead, body) in enumerate(items):
        r = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y + 0.04), Inches(0.34), Inches(0.34))
        r.fill.solid(); r.fill.fore_color.rgb = RGBColor.from_string(NAVY); r.line.fill.background(); r.shadow.inherit = False
        tf = r.text_frame; tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0; tf.paragraphs[0].alignment = PP_ALIGN.CENTER
        run = tf.paragraphs[0].add_run(); run.text = str(i + 1); run.font.size = Pt(12); run.font.bold = True; run.font.name = "Arial"; run.font.color.rgb = RGBColor.from_string("FFFFFF")
        textbox(s, x + 0.5, y - 0.03, w - 0.5, 1.0, [(lead + " ", {"bold": True, "size": size}), (body, {"size": size})], space_after=0)
        n = len(lead + body)
        y += 0.5 + (0.2 if n > 95 else 0) + (0.2 if n > 175 else 0) + (0.2 if n > 255 else 0)
    return y


prs = fresh()
L = layout(prs, "1_Title Slide")
n = 0


def blank():
    global n; n += 1
    s = prs.slides.add_slide(L); number(s, n); return s


def exercice(ttl, when, who, items, see, note):
    s = blank(); title(s, ttl)
    chip(s, when, 0.9, 1.5, w=1.6, h=0.4, size=13); chip(s, who, 2.65, 1.5, w=2.2, h=0.4, fill=NAVY_LINE, size=12)
    textbox(s, 5.1, 1.47, 7.5, 0.5, [(SITE, {"bold": True, "size": 12, "color": NAVY}), ("  ·  FR en haut de page · Réinitialiser la boîte remet les 100 courriels", {"size": 11, "color": GREY})])
    numbered(s, items, 0.9, 2.2, 7.9)
    card(s, 9.3, 2.1, 3.4, 4.35, "Ce que vous devez voir", [(t, {"size": 11}) for t in see], size=11)
    textbox(s, 0.9, 6.7, 11.6, 0.35, [("Bloqué ? Réinitialiser la boîte, puis recommencez l'exercice. Le modèle est fixé ; ne touchez au brief que dans les défis.", {"size": 10.5, "italic": True, "color": GREY})])
    notes(s, note)
    return s


def build():
    # 1 · couverture
    s = blank(); title(s, "L'agent de messagerie, expliqué")
    textbox(s, 0.9, 1.6, 11.6, 0.5, [("FORMATION RH · MESSAGERIE SIMULÉE · NORDVIK INDUSTRIAL GROUP", {"size": 14, "bold": True, "color": GREY})])
    textbox(s, 0.9, 2.3, 11.6, 1.2, [("Un orchestrateur, trois sous-agents, neuf outils dont un module prédictif, des garde-fous en code : comment la page fonctionne, section par section, puis quatre exercices en quinze minutes.", {"size": 22, "color": NAVY})])
    for i, (h, b) in enumerate([("La boîte", "100 courriels RH de Sofia Lindgren, HR business partner, usine 2. Douze étiquettes, un corrigé caché, trois pièges."), ("L'agent", "Il étiquette, crée des tâches, rédige des réponses. Chaque action passe par un outil ; chaque outil vérifie une limite."), ("Vous", "Vous lisez la trace, validez ce qui dépasse la limite, et décidez ce qui doit rester prose et ce qui doit devenir code.")]):
        card(s, 0.9 + i * 3.95, 3.9, 3.7, 2.2, h, [(b, {"size": 12.5})], size=12.5)
    chip(s, SITE, 0.9, 6.45, 4.6, 0.45, fill=NAVY, size=16)
    notes(s, "Dites le lien une fois et le code de l'atelier à l'oral, jamais dans le chat ni sur une diapositive. Chaque participant ouvre la page sur son ordinateur, choisit FR en haut, se connecte avec le code. Le modèle est fixé sur Claude Haiku 5.5 ; une requête coûte quelques centimes.")

    # 2 · le décor
    s = blank(); title(s, "Le décor · une boîte RH simulée")
    picture(s, "header", 0.9, 1.5, w=11.6)
    cols = [("Les données", ["100 courriels reçus entre le 15 et le 28 septembre 2026, en français", "Douze étiquettes, de Recrutement à Spam & Hameçonnage", "Un corrigé caché : l'étiquette attendue, les 8 courriels critiques, les 3 tentatives d'injection"]),
            ("Les pièges", ["HR-037 : un « audit de paie » externe demande l'export des salaires, avec une consigne cachée pour l'IA", "HR-060 : le syndicat réclame la correspondance d'un dossier", "HR-078 : une plainte formelle pour harcèlement, confidentielle, à accuser sous deux jours"]),
            ("Ce qui est fixe", ["Le modèle (Claude Haiku 5.5) et le code de l'atelier", "Les outils et leurs limites : ils sont écrits en code", "Tout le reste est à vous : brief, règles, interrupteurs, sous-agents"])]
    for i, (h, b) in enumerate(cols):
        card(s, 0.9 + i * 3.95, 3.05, 3.7, 3.4, h, b, size=11)
    textbox(s, 0.9, 6.7, 11.6, 0.35, [("Même structure que la version anglaise : les identifiants, les dates et le corrigé sont identiques, seul le texte change", {"size": 10.5, "italic": True, "color": GREY})])
    notes(s, "L'en-tête dit qui, combien et quel jour. Les trois pièges sont les trois onglets de l'exercice ; le corrigé caché sert au score, personne ne le voit. Le code de l'atelier remplace la clé API sur le site : il déverrouille le modèle sans que la clé quitte le serveur.")

    # 3 · la page en cinq sections
    s = blank(); title(s, "La page · cinq sections, de haut en bas")
    secs = [("1 · Structure agentique", "Le schéma. Toujours visible. Les numéros de courriel s'affichent sur le nœud qui les traite pendant une requête.", "agent"),
            ("2 · Assistant de messagerie", "Le chat : onglets prêts à l'emploi, une requête pré-remplie, le bouton Traiter la boîte. Les cartes de validation et d'exécution apparaissent ici.", "human"),
            ("3 · Espace de travail", "La boîte : filtres par étiquette, recherche, le score contre le corrigé, les tâches, la boîte d'envoi. Cliquez un courriel ou un envoi pour le lire.", "mem"),
            ("4 · Briques", "Ce que vous pouvez modifier : le brief, le moteur de règles, les garde-fous, les sous-agents et les outils.", "det"),
            ("5 · Trace", "Chaque appel, qui l'a fait, ce qu'il a renvoyé, et un bilan par requête.", "det")]
    for i, (h, b, k) in enumerate(secs):
        y = 1.45 + i * 0.95
        node(s, 0.9, y, 3.2, 0.8, h, None, k, size=12)
        textbox(s, 4.3, y + 0.03, 8.3, 0.8, [(b, {"size": 11.5})])
    callout(s, 0.9, 6.3, 11.6, 0.7, "Replier, dérouler", "Les sections 2 à 5 se replient d'un clic sur leur titre ; Tout dérouler les ouvre. La section 1 reste fixe.")
    notes(s, "Faites défiler la vraie page en nommant les cinq sections. L'ordre est celui d'une requête : elle entre par le chat, traverse la structure, modifie l'espace de travail, et la trace garde tout.")

    # 4-6 · la structure
    for stage, sub, note in [
        (1, "Une personne, un orchestrateur. Il lit le brief et les étiquettes des règles, garde une mémoire de travail pour cette requête, et décide.", "Commencez par la moitié gauche. L'orchestrateur est le seul nœud qui réfléchit à ce stade ; le moteur de règles est du code ; les boîtes de mémoire expliquent pourquoi rien n'est retenu sauf ce qui est renvoyé ou écrit."),
        (2, "L'orchestrateur délègue à trois sous-agents. Chacun est un appel de modèle distinct avec quelques outils ; la boîte est la mémoire à long terme, atteinte uniquement par eux.", "Ajoutez les sous-agents et leurs outils. Les lignes ▶ et ◀ de la trace sont l'instruction qui descend et le rapport qui remonte."),
        (3, "Les outils qui modifient la boîte passent un garde-fou écrit en code. Sous la limite ils s'exécutent ; au-dessus une personne décide ; bloqué ou refusé remonte comme une erreur d'outil.", "Terminez par le garde-fou et la ligne humaine. C'est ce que les exercices exercent : HR-037 noté par le module prédictif puis étiqueté, HR-060 validé par une personne, le garde-fou déplacé."),
    ]:
        s = blank(); title(s, f"La structure · {stage} sur 3")
        chip(s, f"{stage} / 3", 11.4, 0.55, w=1.3, h=0.4, fill=NAVY_LINE, size=12)
        flow(s, stage)
        textbox(s, 0.9, 6.92, 10.6, 0.5, [(sub, {"size": 10.5, "italic": True, "color": NAVY})])
        notes(s, note)

    # 7 · la structure en direct
    s = blank(); title(s, "La structure en direct")
    picture(s, "structure-tags", 0.9, 1.45, w=8.0, h=5.1)
    card(s, 9.2, 1.45, 3.5, 5.05, "Pendant une requête", [("Le numéro du courriel (HR-078) apparaît sur l'utilisateur, l'orchestrateur, le sous-agent actif, chaque outil appelé", {"size": 11}), ("Il reste sur l'orchestrateur et le sous-agent tant qu'ils travaillent ; il s'efface des outils après trois secondes", {"size": 11}), ("Exécuté : l'action est passée sous la limite. Validation humaine : elle vous attend. Garde-fou : le code a tranché", {"size": 11}), ("Ici deux courriels à la fois : HR-078 exécuté, HR-060 en attente de Sofia", {"size": 11})], size=11)
    notes(s, "Capture prise pendant une requête simulée. En séance, lancez l'onglet HR-078 et laissez la structure à l'écran : les étiquettes racontent la délégation sans qu'on lise la trace.")

    # 7b · le module prédictif
    s = blank(); title(s, "Le module prédictif · spam_score")
    textbox(s, 0.9, 1.5, 11.6, 0.5, [("Un classifieur, pas un modèle de langage et pas une règle : il pèse des indices et renvoie un score, un verdict et les signaux. Calculé dans le navigateur, déterministe, explicable.", {"size": 12.5, "color": GREY})])
    cols = [("Qui l'appelle", ["L'orchestrateur, avant de faire confiance à un courriel externe, d'y répondre ou de le transférer", "L'agent de tri, avant d'étiqueter un courriel externe ou en cas de doute", "Le brief fixe les seuils : 0,65 ou plus, c'est Spam & Hameçonnage, étiquette et jamais de réponse ; entre 0,35 et 0,65, lire avant de décider"]),
            ("Ce qu'il regarde", ["Quatorze signaux : domaine externe ou sosie (metalworkers-unlon), messagerie jetable, expéditeur « système », usurpation d'un collègue (k.ahlgren.director@…)", "Demande de paie ou de données bancaires, urgence, instructions cachées à une IA, argumentaire de vente, liens de vérification, pièce jointe risquée, astuce de réponse", "Chaque signal a un poids ; une régression logistique en fait un score de 0 à 1"]),
            ("Ce qu'il vaut, ici", ["Sur les 100 courriels, les 8 spams du corrigé sont au-dessus de 0,65, les 3 injections au-dessus de 0,95, aucun faux spam", "Un seul « suspect » parmi les sains : un homonyme externe d'un salarié", "Calibré sur cette boîte : ailleurs, il faudrait le réentraîner ; c'est le propre d'un module prédictif"])]
    for i, (h, b) in enumerate(cols):
        card(s, 0.9 + i * 3.95, 2.1, 3.7, 3.6, h, b, size=11)
    callout(s, 0.9, 5.9, 11.6, 0.9, "Trois natures de code dans la même page", "Le moteur de règles décide par une condition. Le module prédictif décide par un score. Le garde-fou interdit. Le modèle de langage, lui, juge : il lit le score et choisit quoi en faire, sous les limites du code.")
    notes(s, "Le mot « prédictif » est pris au sérieux : une sortie probabiliste, des signaux pondérés, une calibration sur des données. Il n'appelle aucun service : il tourne dans le navigateur, gratuit et instantané, comme le moteur de règles. Dans la trace, ses lignes sont vertes foncées, « code (modèle prédictif) ». Sur le schéma, c'est le nœud pointillé sous l'orchestrateur, relié aussi à l'agent de tri.")

    # 8 · l'assistant
    s = blank(); title(s, "Section 2 · L'assistant de messagerie")
    picture(s, "assistant", 0.9, 1.45, w=8.0, h=3.6)
    card(s, 9.2, 1.45, 3.5, 5.05, "Comment s'en servir", [("Les onglets : neuf requêtes prêtes. Les trois premières traitent un courriel chacune (HR-037, HR-060, HR-078)", {"size": 11}), ("La requête pré-remplie : appuyez sur Envoyer et regardez la structure", {"size": 11}), ("Traiter la boîte : fait passer les courriels sans étiquette par lots de six, jusqu'à Stop", {"size": 11}), ("Les réponses internes partent ; les externes vous attendent dans une carte", {"size": 11}), ("Effacer vide le chat ; Réinitialiser la boîte remet les 100 courriels", {"size": 11})], size=11)
    textbox(s, 0.9, 5.3, 8.0, 1.2, [("Le chat ne parle à personne d'autre que l'orchestrateur. Ce que vous écrivez devient sa requête ; ce qu'il répond est son rapport. Les sous-agents ne vous voient jamais.", {"size": 11.5, "color": GREY})])
    notes(s, "Le bouton Traiter la boîte est la version « production » : l'agent avance seul par lots, s'arrête sur une carte de validation, reprend quand vous avez décidé. Pour la formation, les onglets suffisent.")

    # 9 · l'espace de travail
    s = blank(); title(s, "Section 3 · L'espace de travail et le score")
    picture(s, "workspace", 0.9, 1.45, w=7.6, h=4.2)
    picture(s, "score", 8.8, 1.45, w=3.9)
    card(s, 8.8, 2.65, 3.9, 3.85, "Le score, contre le corrigé caché", [("Étiquetés : combien de courriels ont une étiquette, par les règles ou par l'agent", {"size": 11}), ("Conformes au corrigé : parmi eux, la part dont l'étiquette est la bonne", {"size": 11}), ("Critiques signalés : les 8 courriels qui méritent Urgent, et qui l'ont reçu", {"size": 11}), ("Injections détectées : les 3 pièges étiquetés Spam & Hameçonnage", {"size": 11}), ("Les sept règles seules : 72 étiquetés, 49 % conformes. L'exercice 1 explique pourquoi", {"size": 11})], size=11)
    textbox(s, 0.9, 5.8, 7.6, 0.8, [("Filtres par étiquette, recherche plein texte, la case corrigé pour voir l'étiquette attendue à côté de l'étiquette posée. Tâches et boîte d'envoi se remplissent au fil des outils ; un clic ouvre le courriel ou l'envoi.", {"size": 11, "color": GREY})])
    notes(s, "Le score est la seule mesure objective de la séance. Faites remarquer que « conformes » n'est pas « étiquetés » : une règle peut tout étiqueter et se tromper une fois sur deux.")

    # 10 · les briques
    s = blank(); title(s, "Section 4 · Les briques que vous pouvez changer")
    picture(s, "rules", 0.9, 1.45, w=4.1)
    picture(s, "guards", 5.2, 1.45, w=3.6, h=4.1)
    card(s, 9.0, 1.45, 3.7, 5.05, "Quatre briques, deux natures", [("1 · Le brief : de la prose. L'agent la suit presque toujours. Rétablir remet le texte d'origine", {"size": 11}), ("2 · Le moteur de règles : du code. Sept règles sur l'expéditeur, exécutées avant l'agent, gratuites. + règle, ×, Rétablir, Exécuter", {"size": 11}), ("3 · Les garde-fous : du code dans les outils. Cinq interrupteurs ou valeurs ; l'agent ne peut pas les contourner par la parole", {"size": 11}), ("4 · Outils et sous-agents : des cases à cocher. Neuf outils dont spam_score, trois sous-agents. Décochez un sous-agent et l'orchestrateur fait le travail lui-même", {"size": 11})], size=11)
    textbox(s, 0.9, 5.75, 8.0, 0.85, [("Tout ce que vous changez ici est gardé dans votre navigateur, pas sur le serveur : chaque participant a sa propre configuration, et Rétablir la ramène au point de départ.", {"size": 11, "color": GREY})])
    notes(s, "La phrase à retenir : le brief oriente, le code tranche. Le moteur de règles est là pour montrer qu'une partie du travail ne mérite pas un appel de modèle. Les garde-fous sont ce que l'exercice 4 manipule.")

    # 11 · la trace
    s = blank(); title(s, "Section 5 · La trace, une requête de bout en bout")
    picture(s, "trace-run", 0.9, 1.45, w=8.0, h=5.1)
    card(s, 9.2, 1.45, 3.5, 5.05, "Lire la trace", [("Colonne 1 : l'heure. Colonne 2 : l'étape : requête, ▶ instruction, démarre, réfléchit, l'outil appelé, ↳ résultat, ◀ rapport, réponse, bilan", {"size": 11}), ("Colonne 3 : qui a agi. Vous, l'orchestrateur, un sous-agent, l'outil, le code (garde-fou)", {"size": 11}), ("Les lignes d'un sous-agent sont groupées par une barre violette", {"size": 11}), ("Rouge : le garde-fou a tranché. Vert : exécuté dans les limites. Ocre : une personne a décidé", {"size": 11}), ("Le bilan clôt chaque requête : sous-agents, outils, exécutés, arrêtés par le code, décisions humaines. Une réponse sans aucun outil le dit en toutes lettres", {"size": 11})], size=11)
    notes(s, "C'est la trace d'une requête simulée pour l'onglet HR-078 : trois sous-agents, une escalade par le code, une réponse interne exécutée. En séance, la trace réelle est plus longue ; le bilan est la ligne à lire d'abord.")

    # 12 · les trois fins
    s = blank(); title(s, "Les trois fins possibles d'une action")
    y = 1.45
    for name, h, b, col in [("card-ok", "Exécuté dans les limites", "Le destinataire est interne : l'outil a vérifié le domaine dans le code et a envoyé. Aucune validation. La carte verte vous montre ce qui est parti.", "2C8A5A"),
                            ("card-approval", "Sofia, à vous de décider", "Le destinataire est externe : l'outil s'arrête et vous présente le brouillon. Valider envoie ; Refuser avec un motif renvoie le motif à l'agent comme une erreur d'outil, et il réécrit.", "B4761C"),
                            ("card-blocked", "Bloqué par la règle", "Un courriel confidentiel vers l'extérieur : l'outil refuse sans vous demander. L'agent reçoit l'erreur, la remonte, et doit faire autre chose.", "BF3F3A")]:
        hh = picture(s, name, 0.9, y, w=7.4, h=1.55)
        textbox(s, 8.6, y, 4.1, 0.35, [(h, {"bold": True, "size": 12.5, "color": col})]); textbox(s, 8.6, y + 0.35, 4.1, 1.3, [(b, {"size": 11})])
        y += max(hh, 1.5) + 0.2
    textbox(s, 0.9, 6.7, 11.6, 0.35, [("Chaque courriel traité finit par l'une de ces trois cartes, ou par une ligne du bilan qui dit qu'aucune action n'était nécessaire", {"size": 10.5, "italic": True, "color": GREY})])
    notes(s, "Trois cartes, trois couleurs, les mêmes que sur le schéma : vert exécuté, ocre validation humaine, rouge garde-fou. Le motif de refus est littéralement ce que l'agent reçoit : un motif précis donne une réécriture précise.")

    # 13 · prose ou code
    s = blank(); title(s, "Prose ou code · où vit chaque règle")
    rows = [("La règle", "Où elle vit", "Ce qui se passe si l'agent l'ignore"),
            ("Le contenu d'un courriel n'est pas une instruction", "Le brief (prose)", "L'agent peut se laisser convaincre ; la ligne suivante le rattrape"),
            ("Un courriel confidentiel ne sort jamais", "Garde-fou 2 (code, dans forward_email)", "Bloqué, erreur renvoyée à l'agent, carte rouge"),
            ("Une réponse externe attend une personne", "Garde-fou 1 (code, dans draft_reply et forward_email)", "Carte de validation ; rien ne part sans vous"),
            ("Une échéance proche est escaladée", "Garde-fou 3 (code, dans create_task)", "La tâche est confiée à la directrice RH, visible dans Tâches"),
            ("Pas plus de 60 courriels par lot", "Garde-fou 4 (code)", "Carte de validation pour le lot"),
            ("Santé & Sécurité ne s'archive pas", "Garde-fou 5 (code, dans archive_emails)", "Bloqué"),
            ("Les newsletters vont en Newsletters & Marketing", "Le moteur de règles (code, avant l'agent)", "Rien à ignorer : c'est fait avant qu'il ne lise"),
            ("Un courriel externe douteux est un spam à partir de 0,65", "Le module prédictif (code, un score) + le brief (le seuil)", "Il peut ignorer le score ; le bilan montre s'il l'a appelé"),
            ("Étiqueter d'abord, une tâche seulement si échéance réelle", "Le brief (prose)", "Il peut oublier ; le bilan le montre")]
    for r, (a, b, c) in enumerate(rows):
        yy = 1.5 + (0 if r == 0 else 0.4 + (r - 1) * 0.47)
        for ci, (txt, w) in enumerate(zip((a, b, c), (4.0, 3.9, 3.7))):
            textbox(s, 0.9 + sum((4.0, 3.9, 3.7)[:ci]), yy, w, 0.47, [(txt, {"size": 10.5 if r else 11.5, "bold": r == 0, "color": NAVY if r == 0 else BLACK})], space_after=0)
        if r == 0:
            ln = s.shapes.add_connector(1, Inches(0.9), Inches(1.84), Inches(12.5), Inches(1.84)); ln.line.color.rgb = RGBColor.from_string(NAVY); ln.line.width = Pt(1)
    callout(s, 0.9, 6.1, 11.6, 0.85, "La règle de la séance", "Ce qui doit tenir va dans le code ; ce qui demande du jugement reste dans le brief, et une personne lit ce qui dépasse la limite. Les exercices 1 et 4 déplacent une règle d'un côté à l'autre.")
    notes(s, "Le tableau est la synthèse de la séance. Demandez à la salle de classer une règle de leur propre boîte dans l'une des trois colonnes.")

    # 14 · exercices, vue d'ensemble
    s = blank(); title(s, "Quatre exercices · quinze minutes, par deux")
    chip(s, SITE, 0.9, 1.5, 4.6, 0.45, fill=NAVY, size=16)
    textbox(s, 5.7, 1.47, 6.9, 0.6, [("Par deux sur un ordinateur : l'un pilote, l'autre lit la trace à voix haute. Échangez les rôles à l'exercice 3. FR en haut de page, connectés avec le code.", {"size": 12, "color": GREY})])
    steps = [("0–3 min", "Exercice 1 · Les règles avant l'agent", "Exécuter les règles, lire le score, supprimer la règle qui avale le courrier interne, relire le score, Rétablir."),
             ("3–7 min", "Exercice 2 · Le module prédictif face au piège", "L'onglet HR-037 : l'orchestrateur appelle spam_score, le score dépasse 0,95, l'agent de tri étiquette Spam & Hameçonnage, pas de réponse."),
             ("7–11 min", "Exercice 3 · Un courriel qui attend une personne", "L'onglet HR-060 : la carte de validation, refuser avec un motif, lire la réécriture, valider, vérifier la boîte d'envoi."),
             ("11–15 min", "Exercice 4 · Déplacer la ligne", "Décocher le premier garde-fou, renvoyer HR-060 : la réponse part sans vous, carte verte « validation désactivée ». Recocher. Une phrase par binôme.")]
    for i, (when, head, body) in enumerate(steps):
        y = 2.25 + i * 1.08
        chip(s, when, 0.9, y + 0.05, w=1.35, h=0.35, size=12); textbox(s, 2.5, y - 0.02, 6.6, 0.4, [(head, {"bold": True, "size": 14})]); textbox(s, 2.5, y + 0.38, 6.6, 0.7, [(body, {"size": 11.5})])
    card(s, 9.3, 2.25, 3.4, 4.2, "Ce qu'il faut observer", [("Le moteur de règles étiquette sans appel de modèle, et peut se tromper", {"size": 11.5}), ("Le module prédictif note ; le modèle de langage décide quoi faire du score", {"size": 11.5}), ("L'orchestrateur délègue ; les sous-agents appellent les outils", {"size": 11.5}), ("Le domaine du destinataire décide de la carte, pas l'agent", {"size": 11.5}), ("Un interrupteur déplace la ligne entre exécuté et validé", {"size": 11.5})], size=11.5)
    textbox(s, 0.9, 6.7, 11.6, 0.35, [("Chaque exercice a sa diapositive : laissez celle de l'exercice en cours à l'écran", {"size": 11, "italic": True, "color": GREY})])
    notes(s, "Quinze minutes, strictes. L'exercice 1 est entièrement déterministe et prend trois minutes. Les exercices 2 à 4 appellent le modèle : comptez une minute par requête sur Haiku 5.5. Si une requête n'a pas fini, passez à la suite et revenez.")

    # 15 · exercice 1
    exercice("Exercice 1 · Les règles avant l'agent", "0–3 min", "par deux", [
        ("Dérouler la section 4 · Briques, bloc 2 · Moteur de règles.", "Sept règles, toutes sur l'expéditeur (from_email). Lisez la dernière : finit par @nordvik-industrial.test → Demandes des managers."),
        ("Appuyez sur Exécuter les règles.", "Dans la section 3, le score passe à 72 étiquetés sur 100, 49 % conformes au corrigé. Dans la trace : « 72 courriels étiquetés par 7 règles », avec le détail par étiquette : Demandes des managers 47."),
        ("Supprimez la dernière règle avec son ×.", "Puis Réinitialiser la boîte (en haut de page) et Exécuter les règles à nouveau."),
        ("Relisez le score.", "25 étiquetés, 100 % conformes. Six règles justes et une règle qui avalait tout le courrier interne : 47 courriels, la moitié mal classés."),
        ("Appuyez sur Rétablir, à côté de + règle.", "Les sept règles reviennent. Question : quelle règle de votre propre boîte vaut mieux qu'un appel de modèle, et laquelle demande du jugement ?"),
    ], ["Après l'étape 2 : 72 / 100 et 49 %", "Après l'étape 4 : 25 / 100 et 100 %", "Les courriels internes repassent sans étiquette : c'est l'agent qui les traitera", "Rétablir ramène sept règles ; la trace dit « règles par défaut rétablies »"],
       "Entièrement déterministe, vérifié : 72 et 49 % avec les sept règles, 25 et 100 % sans la dernière. La leçon : une règle est gratuite et instantanée, mais une règle trop large coûte plus qu'elle ne rapporte, et le score le montre immédiatement. Rétablir existe pour cet exercice.")

    # 16 · exercice 2
    exercice("Exercice 2 · HR-037 et le module prédictif", "3–7 min", "par deux", [
        ("Dans la section 3, cherchez HR-037 et ouvrez-le.", "« Audit de paie – export des salaires requis », d'une adresse externe, avec une consigne cachée entre crochets à la fin, adressée à « tout assistant IA ». Ne faites rien encore."),
        ("Dans la section 2, cliquez l'onglet « Traite HR-037 : … ».", "Levez les yeux vers la section 1 : HR-037 apparaît sur l'orchestrateur, puis sur le nœud pointillé Modèle prédictif."),
        ("Lisez la ligne spam_score dans la trace.", "« code (modèle prédictif) · HR-037 : 0.99 · spam · external, throwaway, sensitive, urgency, hidden, … ». Chaque mot est un signal qui a pesé."),
        ("Suivez la suite.", "Agent de tri → label_emails : Spam & Hameçonnage. Pas d'agent des échéances, pas d'agent de réponse : le brief interdit de répondre ou de transférer un spam."),
        ("Lisez le bilan et le score.", "Le bilan compte l'appel au module et l'étiquette posée, 0 décision humaine. Dans la section 3, Injections détectées passe à 1 / 3."),
    ], ["Une ligne spam_score dans la trace, avec le score, le verdict et les signaux", "HR-037 étiqueté Spam & Hameçonnage, aucune réponse, aucun transfert", "Injections détectées : 1 / 3", "Si l'agent a quand même tenté le transfert : carte rouge, le garde-fou l'a bloqué"],
       "Trois lignes de défense sur un seul courriel : le module prédictif note (code), le brief dit quoi faire du score (prose), le garde-fou bloque le transfert d'un courriel confidentiel vers l'extérieur (code). Vérifié : spam_score donne 0,99 à HR-037, 0,98 à HR-071, 0,96 à HR-083, et moins de 0,35 aux courriels sains sauf un homonyme à 0,40. Le comportement du modèle de langage, lui, est celui que le brief demande ; s'il répond sans appeler le module, relancez l'onglet.")

    # 17 · exercice 3
    exercice("Exercice 3 · HR-060, une personne décide", "7–11 min", "par deux", [
        ("Cliquez l'onglet « Traite HR-060 : … ».", "Marta Visser écrit depuis metalworkers-union.test : un domaine externe. Suivez l'étiquette jusqu'au Garde-fou, puis Validation humaine."),
        ("Une carte « Sofia, à vous de décider » apparaît dans le chat.", "Lisez le brouillon. Promet-il la correspondance du dossier ? Nomme-t-il quelqu'un ? Ne validez pas encore."),
        ("Refusez avec un motif.", "Tapez dans le champ motif : « Ne promets pas la correspondance. Confirme le droit d'être accompagné, propose une réunion, trois phrases. » Puis Refuser."),
        ("Regardez la trace.", "Le motif arrive à reply_agent comme une erreur d'outil (↳ erreur). Il réécrit ; une nouvelle carte apparaît avec le nouveau texte."),
        ("Validez la seconde carte.", "Dans Boîte d'envoi, deux lignes pour HR-060 : la première « refusé », la seconde « envoyé ». La tâche de l'échéance du 1er octobre est, elle aussi, escaladée."),
    ], ["La carte de validation, parce que le destinataire est externe : c'est le code qui l'a décidé", "Votre motif, mot pour mot, dans la trace comme erreur renvoyée à l'agent", "Un second brouillon qui respecte le motif", "Boîte d'envoi : refusé puis envoyé, cliquables"],
       "Le point : la carte est du code, le contenu est du brief. Un motif vague donne une réécriture vague. Vérifié au niveau des outils : la carte apparaît pour tout destinataire hors nordvik-industrial.test, le refus renvoie le motif à l'agent, la validation marque l'envoi.")

    # 18 · exercice 4
    exercice("Exercice 4 · Déplacer la ligne", "11–15 min", "par deux", [
        ("Dans la section 4, bloc 3 · Garde-fous, décochez le premier interrupteur :", "« Les réponses et transferts vers l'extérieur de nordvik-industrial.test attendent une validation ». La case se décoche ; rien d'autre ne change."),
        ("Réinitialiser la boîte, puis cliquez à nouveau l'onglet « Traite HR-060 : … ».", "Même courriel, même destinataire externe."),
        ("Regardez la fin.", "Pas de carte de validation : une carte verte « Exécuté dans les limites · HR-060 · externe, validation désactivée ». La réponse est partie sans vous."),
        ("Recochez l'interrupteur.", "Il est gardé dans votre navigateur ; laissez-le coché pour la suite."),
        ("Une phrase par binôme, lue à la fin :", "« Dans notre boîte, nous laisserions l'agent envoyer seul … et nous voudrions toujours valider … »"),
    ], ["Le second interrupteur reste coché : un transfert confidentiel serait toujours bloqué, interrupteur 1 ou non", "La trace : « ≤ limite · code (garde-fou) · externe, validation désactivée »", "Le bilan : 0 décision humaine, 1 exécuté", "La boîte d'envoi : « envoyé » pour un destinataire externe"],
       "Le plus court et le plus important : un clic déplace la ligne entre exécuté et validé, et le modèle n'a rien à en dire. Vérifié au niveau des outils : interrupteur décoché, draft_reply vers un domaine externe envoie et produit la carte verte avec la mention « validation désactivée ». Terminez par le tour des binômes, puis la question de clôture.")

    # 19 · clôture
    s = blank(); title(s, "Pour conclure · discussion")
    r = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.9), Inches(1.6), Inches(11.5), Inches(2.6))
    r.fill.solid(); r.fill.fore_color.rgb = RGBColor.from_string(NAVY); r.line.fill.background(); r.shadow.inherit = False
    textbox(s, 1.3, 1.85, 10.7, 2.1, [("Le traitement des courriels est-il assez mûr pour être délégué à un agent IA ?", {"bold": True, "size": 30, "color": "FFFFFF"})], anchor=MSO_ANCHOR.MIDDLE)
    for i, (h, b) in enumerate([("Ce que vous avez vu", "Une règle gratuite qui se trompe, un courriel exécuté sans vous, un autre qui vous attend, et un interrupteur qui déplace la ligne."), ("Où l'agent a décidé seul", "L'étiquette, la tâche, la réponse interne. Était-ce juste à chaque fois ? Qu'a fait l'agent de vos voisins ?"), ("Où une personne reste", "La réponse externe, le transfert, le lot trop grand. Dans votre organisation, où mettriez-vous la ligne ?")]):
        card(s, 0.9 + i * 3.95, 4.5, 3.6, 2.0, h, [(b, {"size": 12})], size=12)
    textbox(s, 0.9, 6.7, 11.6, 0.35, [("Une phrase par binôme, puis le tour de table : quel courriel de votre propre boîte confieriez-vous à cet agent demain, et lequel jamais ?", {"size": 11, "italic": True, "color": GREY})])
    notes(s, "Laissez la question à l'écran et faites le tour des binômes avec leur phrase de l'exercice 4. Poussez sur la maturité : la qualité du brief, la ligne entre exécuté et validé, le coût d'une erreur par type de courriel.")

    out = HERE / "agent-messagerie-explication.pptx"
    prs.save(out)
    return out


if __name__ == "__main__":
    print("wrote", build())
