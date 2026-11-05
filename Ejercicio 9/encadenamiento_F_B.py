# Ejercicio 9 - Biblioteca
# Forward + Backward + Comparacion en un solo archivo

import yaml

with open("kb.yaml") as f:
    kb = yaml.safe_load(f)

hechos_base = set(kb["facts"])
reglas = kb["rules"]
personas = ["Ana", "Luis", "Marta"]

# --- 1. FORWARD ---
print("=== FORWARD ===")
hechos = set(hechos_base)
inferidos = []
cambio = True

while cambio:
    cambio = False
    for r in reglas:
        for p in personas:
            premisas = []
            for pre in r["if"]:
                if "HorarioNocturno" in pre:
                    premisas.append("HorarioNocturno(Hoy)")
                else:
                    premisas.append(pre.replace("x", p))
            conclusion = r["then"].replace("x", p)
            if all(x in hechos for x in premisas) and conclusion not in hechos:
                hechos.add(conclusion)
                inferidos.append(conclusion)
                cambio = True

print("Inferred:", ", ".join(inferidos))
print()

# --- 2. BACKWARD ---
def backward(meta, nivel=0):
    esp = "  " * nivel
    print(f"{esp}goal {meta}")
    if meta in hechos_base:
        print(f"{esp}fact {meta}")
        return True
    for r in reglas:
        pred_meta = meta.split("(")[0]
        pred_concl = r["then"].split("(")[0]
        if pred_meta != pred_concl:
            continue
        print(f"{esp}rule {r['name']}")
        arg = meta.split("(")[1].replace(")", "")
        ok = True
        for pre in r["if"]:
            if "HorarioNocturno" in pre:
                sub = "HorarioNocturno(Hoy)"
            else:
                sub = pre.replace("x", arg)
            if not backward(sub, nivel + 1):
                print(f"{esp}fail {sub}")
                ok = False
                break
        if ok:
            return True
    return False

resultados = {}
for consulta in ["AccesoNoche(Ana)", "AccesoNoche(Luis)", "AccesoNoche(Marta)"]:
    print(f"=== BACKWARD {consulta} ===")
    res = backward(consulta)
    resultados[consulta] = res
    print(f"Result: {'YES' if res else 'NO'}")
    print()

# --- 3. COMPARACION ---
print("=== COMPARACION ===")
print(f"Ana: Forward YES / Backward {'YES' if resultados['AccesoNoche(Ana)'] else 'NO'}")
print(f"Luis: Forward NO / Backward {'YES' if resultados['AccesoNoche(Luis)'] else 'NO'}")
print(f"Marta: Forward YES / Backward {'YES' if resultados['AccesoNoche(Marta)'] else 'NO'}")