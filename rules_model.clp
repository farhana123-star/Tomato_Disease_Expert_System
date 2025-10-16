; ==========================================
; TOMATO DISEASE EXPERT SYSTEM - WITH CERTAINTY FACTORS (CF)
; Description: Expert system to diagnose tomato plant diseases based on symptoms
; CFs are defined as a float from 0.0 to 1.0.
; ==========================================

; ==============================
; TEMPLATES
; ==============================
(deftemplate symptom
   (slot name)
)

; UPDATED: Added confidence slot for Certainty Factor
(deftemplate disease
   (slot name)
   (slot confidence (default 0.0) (type FLOAT) (range 0.0 1.0))
)

; ==========================================
; 1️⃣ EARLY BLIGHT (Alternaria solani)
; ==========================================
(defrule early-blight-1
   (symptom (name yellow-leaves))
   (symptom (name brown-spots))
   =>
   (assert (disease (name early-blight) (confidence 0.65)))
   (printout t "Diagnosis: Early Blight (CF: 0.65)" crlf))

(defrule early-blight-2-defining
   (symptom (name concentric-rings))
   (symptom (name lower-leaves-affected))
   =>
   (assert (disease (name early-blight) (confidence 0.90)))
   (printout t "Diagnosis: Early Blight (CF: 0.90)" crlf))

(defrule early-blight-3
   (symptom (name leaf-drop))
   (symptom (name stem-lesions))
   =>
   (assert (disease (name early-blight) (confidence 0.75)))
   (printout t "Diagnosis: Early Blight (CF: 0.75)" crlf))


; ==========================================
; 2️⃣ LATE BLIGHT (Phytophthora infestans)
; ==========================================
(defrule late-blight-1
   (symptom (name gray-mold))
   (symptom (name black-lesions))
   =>
   (assert (disease (name late-blight) (confidence 0.80)))
   (printout t "Diagnosis: Late Blight (CF: 0.80)" crlf))

(defrule late-blight-2-defining
   (symptom (name water-soaked-spots))
   (symptom (name stem-lesions))
   (symptom (name fruit-rot))
   =>
   (assert (disease (name late-blight) (confidence 0.95)))
   (printout t "Diagnosis: Late Blight (CF: 0.95)" crlf))


; ==========================================
; 3️⃣ SEPTORIA LEAF SPOT (Septoria lycopersici)
; ==========================================
(defrule septoria-leaf-spot-1
   (symptom (name white-mold-on-leaves))
   (symptom (name gray-centers))
   =>
   (assert (disease (name septoria-leaf-spot) (confidence 0.85)))
   (printout t "Diagnosis: Septoria Leaf Spot (CF: 0.85)" crlf))

(defrule septoria-leaf-spot-2
   (symptom (name dark-margins))
   (symptom (name small-circular-spots))
   =>
   (assert (disease (name septoria-leaf-spot) (confidence 0.70)))
   (printout t "Diagnosis: Septoria Leaf Spot (CF: 0.70)" crlf))


; ==========================================
; 4️⃣ BACTERIAL SPOT (Xanthomonas campestris)
; ==========================================
(defrule bacterial-spot-1
   (symptom (name lower-leaves-yellow))
   (symptom (name small-water-soaked-spots))
   =>
   (assert (disease (name bacterial-spot) (confidence 0.75)))
   (printout t "Diagnosis: Bacterial Spot (CF: 0.75)" crlf))

(defrule bacterial-spot-2
   (symptom (name rough-leaf-surface))
   (symptom (name black-spots-on-fruit))
   =>
   (assert (disease (name bacterial-spot) (confidence 0.85)))
   (printout t "Diagnosis: Bacterial Spot (CF: 0.85)" crlf))


; ==========================================
; 5️⃣ FUSARIUM WILT (Fusarium oxysporum)
; ==========================================
(defrule fusarium-wilt-1-defining
   (symptom (name yellowing-one-side))
   (symptom (name wilting-leaves))
   =>
   (assert (disease (name fusarium-wilt) (confidence 0.95)))
   (printout t "Diagnosis: Fusarium Wilt (CF: 0.95)" crlf))

(defrule fusarium-wilt-2
   (symptom (name brown-vascular-tissue))
   (symptom (name yellowing-lower-leaves))
   =>
   (assert (disease (name fusarium-wilt) (confidence 0.80)))
   (printout t "Diagnosis: Fusarium Wilt (CF: 0.80)" crlf))


; ==========================================
; 6️⃣ VERTICILLIUM WILT (Verticillium albo-atrum)
; ==========================================
(defrule verticillium-wilt-1
   (symptom (name yellowing-lower-leaves))
   (symptom (name leaf-browning))
   =>
   (assert (disease (name verticillium-wilt) (confidence 0.75)))
   (printout t "Diagnosis: Verticillium Wilt (CF: 0.75)" crlf))

(defrule verticillium-wilt-2
   (symptom (name small-dark-spots))
   (symptom (name v-shaped-lesions))
   =>
   (assert (disease (name verticillium-wilt) (confidence 0.60)))
   (printout t "Diagnosis: Verticillium Wilt (CF: 0.60)" crlf))


; ==========================================
; 7️⃣ TOMATO MOSAIC VIRUS (ToMV)
; ==========================================
(defrule tmv-1-defining
   (symptom (name light-dark-patches))
   (symptom (name mottled-leaves))
   =>
   (assert (disease (name tomato-mosaic-virus) (confidence 0.90)))
   (printout t "Diagnosis: Tomato Mosaic Virus (CF: 0.90)" crlf))

(defrule tmv-2
   (symptom (name leaf-distortion))
   (symptom (name twisted-leaves))
   =>
   (assert (disease (name tomato-mosaic-virus) (confidence 0.75)))
   (printout t "Diagnosis: Tomato Mosaic Virus (CF: 0.75)" crlf))


; ==========================================
; 8️⃣ TOMATO YELLOW LEAF CURL VIRUS (TYLCV)
; ==========================================
(defrule tylcv-1-defining
   (symptom (name upward-curling-leaves))
   (symptom (name yellow-veins))
   (symptom (name reduced-leaf-size))
   =>
   (assert (disease (name tomato-yellow-leaf-curl-virus) (confidence 0.98)))
   (printout t "Diagnosis: Tomato Yellow Leaf Curl Virus (CF: 0.98)" crlf))

(defrule tylcv-2
   (symptom (name stunted-growth))
   (symptom (name flower-drop))
   =>
   (assert (disease (name tomato-yellow-leaf-curl-virus) (confidence 0.70)))
   (printout t "Diagnosis: Tomato Yellow Leaf Curl Virus (CF: 0.70)" crlf))


; ==========================================
; 9️⃣ ANTHRACNOSE (Colletotrichum coccodes)
; ==========================================
(defrule anthracnose-1-defining
   (symptom (name sunken-dark-spots-on-fruit))
   (symptom (name fruit-rot))
   =>
   (assert (disease (name anthracnose) (confidence 0.90)))
   (printout t "Diagnosis: Anthracnose (CF: 0.90)" crlf))


; ==========================================
; 🔟 TARGET SPOT (Corynespora cassiicola)
; ==========================================
(defrule target-spot-1
   (symptom (name yellow-halos))
   (symptom (name small-dark-spots))
   =>
   (assert (disease (name target-spot) (confidence 0.70)))
   (printout t "Diagnosis: Target Spot (CF: 0.70)" crlf))


; ==========================================
; 1️⃣1️⃣ BACTERIAL CANKER (Clavibacter michiganensis)
; ==========================================
(defrule bacterial-canker-1
   (symptom (name wilting-leaves))
   (symptom (name yellowing-lower-leaves))
   =>
   (assert (disease (name bacterial-canker) (confidence 0.60)))
   (printout t "Diagnosis: Bacterial Canker (CF: 0.60)" crlf))


; ==========================================
; 1️⃣2️⃣ POWDERY MILDEW (Erysiphe spp.)
; ==========================================
(defrule powdery-mildew-1-defining
   (symptom (name white-powder-on-leaves))
   (symptom (name curled-leaves))
   =>
   (assert (disease (name powdery-mildew) (confidence 0.95)))
   (printout t "Diagnosis: Powdery Mildew (CF: 0.95)" crlf))


; ==========================================
; 1️⃣3️⃣ BLOSSOM END ROT (Non-Infectious)
; ==========================================
(defrule blossom-end-rot-defining
   (symptom (name dark-sunken-spot-bottom-fruit))
   (symptom (name leathery-texture-fruit))
   =>
   (assert (disease (name blossom-end-rot) (confidence 1.0)))
   (printout t "Diagnosis: Blossom-End Rot (CF: 1.0)" crlf))


; ==========================================
; 1️⃣4️⃣ SOUTHERN BLIGHT (Sclerotium rolfsii)
; ==========================================
(defrule southern-blight-1-defining
   (symptom (name white-fungal-growth-soil-line))
   (symptom (name wilting-leaves))
   =>
   (assert (disease (name southern-blight) (confidence 0.98)))
   (printout t "Diagnosis: Southern Blight (CF: 0.98)" crlf))


; ==========================================
; 1️⃣5️⃣ GRAY LEAF SPOT (Stemphylium spp.)
; ==========================================
(defrule gray-leaf-spot-1-defining
   (symptom (name rectangular-gray-spots))
   (symptom (name yellow-halos))
   =>
   (assert (disease (name gray-leaf-spot) (confidence 0.85)))
   (printout t "Diagnosis: Gray Leaf Spot (CF: 0.85)" crlf))


; ==========================================
; 1️⃣6️⃣ SUNSCALD (Non-Infectious)
; ==========================================
(defrule sunscald-1
   (symptom (name white-patches-on-fruit))
   =>
   (assert (disease (name sunscald) (confidence 0.80)))
   (printout t "Diagnosis: Sunscald (CF: 0.80)" crlf))


; ==========================================
; 1️⃣7️⃣ TOMATO RUST (Puccinia spp.)
; ==========================================
(defrule tomato-rust-1-defining
   (symptom (name brown-pustules-underside))
   =>
   (assert (disease (name tomato-rust) (confidence 0.90)))
   (printout t "Diagnosis: Tomato Rust (CF: 0.90)" crlf))


; ==========================================
; 1️⃣8️⃣ ROOT-KNOT NEMATODE (Meloidogyne spp.)
; ==========================================
(defrule root-knot-nematode-1-defining
   (symptom (name root-galls))
   (symptom (name wilting-on-hot-days))
   =>
   (assert (disease (name root-knot-nematode) (confidence 0.95)))
   (printout t "Diagnosis: Root-Knot Nematode (CF: 0.95)" crlf))


; ==========================================
; 1️⃣9️⃣ NITROGEN DEFICIENCY (Non-Infectious)
; ==========================================
(defrule nitrogen-deficiency-1-defining
   (symptom (name yellowing-old-leaves))
   (symptom (name stunted-plant))
   =>
   (assert (disease (name nitrogen-deficiency) (confidence 0.90)))
   (printout t "Diagnosis: Nitrogen Deficiency (CF: 0.90)" crlf))
