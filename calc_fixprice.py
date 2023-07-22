import logging
logging.getLogger('stl').setLevel(logging.ERROR)
from stl import mesh
import os
import csv
from tqdm import tqdm

Source_Folder = os.path.join(os.path.dirname(__file__), "STL_Files")
Destination_File = os.path.join(os.path.dirname(__file__), "volume.csv")

# Densities in g/cm^3
density_silver_935 = 10.5
density_gold_333 = 11.5
density_gold_586 = 14.2

# Price Silver and Gold in €/g
material_price_silver_935 = 1
material_price_gold_333 = 21.4
material_price_gold_586 = 37.7

# Profit multiplicator, cost of manufacturing, wage per hour and tax
profit_multiplicator = 1.5
cost_manufacturing = 14.9
wage_hour = 65
tax = 0.19

def stl_names():
    stl_files = []
    for file in os.listdir(Source_Folder):
        if file.endswith(".stl") and not file.startswith("._"):
            stl_files.append(file)
    return stl_files

def calculate_volume_and_weight(file):
    your_mesh = mesh.Mesh.from_file(os.path.join(Source_Folder, file))
    volume, cog, inertia = your_mesh.get_mass_properties()
    volume_cm3 = volume / 1000
    weight_silver_935 = volume_cm3 * density_silver_935
    weight_gold_333 = volume_cm3 * density_gold_333
    weight_gold_586 = volume_cm3 * density_gold_586
    return volume, weight_silver_935, weight_gold_333, weight_gold_586

def calculate_price(weight_silver_935, weight_gold_333, weight_gold_586, material_price_silver_935, material_price_gold_333, material_price_gold_586):
    price_silver_935 = (material_price_silver_935 * weight_silver_935 * profit_multiplicator + cost_manufacturing + wage_hour) * (1 + tax)
    price_gold_333 = (material_price_gold_333 * weight_gold_333 * profit_multiplicator + cost_manufacturing + wage_hour) * (1 + tax)
    price_gold_586 = (material_price_gold_586 * weight_gold_586 * profit_multiplicator + cost_manufacturing + wage_hour) * (1 + tax)
    
    
    profit_silver_935 = price_silver_935 - (material_price_silver_935 * weight_silver_935 + cost_manufacturing)
    profit_gold_333 = price_gold_333 - (material_price_gold_333 * weight_gold_333 + cost_manufacturing)
    profit_gold_586 = price_gold_586 - (material_price_gold_586 * weight_gold_586 + cost_manufacturing)
    
    return price_silver_935, price_gold_333, price_gold_586, profit_silver_935, profit_gold_333, profit_gold_586
def main():
    stl_files = stl_names()

    with open(Destination_File, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["Filename", "Volume", "Weight Silver 935", "Weight Gold 333", "Weight Gold 586", "Price Silver 935", "Price Gold 333", "Price Gold 586", "Profit Silver 935", "Profit Gold 333", "Profit Gold 586"])

        for file in tqdm(stl_files, desc="Processing STL files"):
            volume, weight_silver_935, weight_gold_333, weight_gold_586 = calculate_volume_and_weight(file)
            price_silver_935, price_gold_333, price_gold_586, profit_silver_935, profit_gold_333, profit_gold_586 = calculate_price(weight_silver_935, weight_gold_333, weight_gold_586, material_price_silver_935, material_price_gold_333, material_price_gold_586)
            csvwriter.writerow([file, volume, weight_silver_935, weight_gold_333, weight_gold_586, price_silver_935, price_gold_333, price_gold_586, profit_silver_935, profit_gold_333, profit_gold_586])
    
if __name__ == "__main__":
    main()
