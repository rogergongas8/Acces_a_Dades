import csv

# Nombres de los archivos
uf1_file = "Notas_Alumnos_UF1.csv"
uf2_file = "Notas_Alumnos_UF2.csv"
output_file = "notas_alumnos_combinadas.csv"

uf1_data = {}
uf2_data = {}

# Abrimos el primer CSV
with open(uf1_file, 'r', newline='', encoding='latin-1') as f1:
    reader = csv.DictReader(f1, delimiter=';')
    for row in reader:
        student_id = row.get("Id", "").strip()
        if student_id:
            uf1_data[student_id] = row

# Abrimos el segundo CSV
with open(uf2_file, 'r', newline='', encoding='latin-1') as f2:
    reader = csv.DictReader(f2, delimiter=';')
    for row in reader:
        student_id = row.get("Id", "").strip()
        if student_id:
            uf2_data[student_id] = row

all_ids = set(uf1_data.keys()).union(uf2_data.keys())

fieldnames = ["Id", "Nombre", "Apellidos", "Nota_UF1", "Nota_UF2"]

with open(output_file, 'w', newline='', encoding='latin-1') as out:
    writer = csv.DictWriter(out, fieldnames=fieldnames, delimiter=';')
    writer.writeheader()

    for student_id in sorted(all_ids, key=int):
        uf1 = uf1_data.get(student_id, {})
        uf2 = uf2_data.get(student_id, {})

        row = {
            "Id": student_id,
            "Nombre": uf1.get("Nombre", uf2.get("Nombre", "")),
            "Apellidos": uf1.get("Apellidos", uf2.get("Apellidos", "")),

            "Nota_UF1": uf1.get("UF1", ""),
            "Nota_UF2": uf2.get("UF2", "")
        }

        writer.writerow(row)

print(f"Archivo '{output_file}' creado correctamente con {len(all_ids)} alumnos.")