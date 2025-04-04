#!/usr/bin/env python3
import os
import re
import matplotlib.pyplot as plt

RESULTS_DIR = "results"
OUTPUT_DIR = "plots"

def parse_filename(filename):
    """
    Given a filename like:
        gemini-2.0-flash-len0.25-T0.2-results.txt
    extract:
        model = "gemini-2.0-flash"
        proportion = 0.25
        temperature = 0.2
    """
    basename = os.path.splitext(os.path.basename(filename))[0]
    match = re.match(r"^(.*?)-len(.*?)-T(.*?)-results$", basename)
    if not match:
        return None, None, None
    model_str, prop_str, temp_str = match.groups()

    try:
        proportion = float(prop_str)
        temperature = float(temp_str)
    except ValueError:
        proportion = None
        temperature = None
    return model_str, proportion, temperature

def parse_mean_from_file(filepath):
    """
    Reads the file and extracts the line that starts with "mean"
    (e.g., "mean 0.561") and returns the numeric value.
    Returns None if not found.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip().lower()
            if line.startswith("mean"):
                parts = line.split()
                if len(parts) >= 2:
                    try:
                        return float(parts[1])
                    except ValueError:
                        pass
    return None

def gather_results(results_dir=RESULTS_DIR):
    """
    Gathers all (model, proportion, temperature, mean) data from
    result files in the specified directory.
    Returns a list of dicts with keys: model, proportion, temperature, mean.
    """
    data = []
    for filename in os.listdir(results_dir):
        if not filename.endswith(".txt"):
            continue
        filepath = os.path.join(results_dir, filename)
        model, proportion, temperature = parse_filename(filename)
        if model is None or proportion is None or temperature is None:
            continue

        mean_val = parse_mean_from_file(filepath)
        if mean_val is not None:
            data.append({
                "model": model,
                "proportion": proportion,
                "temperature": temperature,
                "mean": mean_val
            })
    return data

def plot_all_combinations(data):
    """
    Plots one figure with lines for each (model + temperature) combination.
    x-axis = proportion, y-axis = mean.
    Legend is sorted first by model, then by temperature.
    """
    # Group data by (model, temperature) => [(proportion, mean), ...]
    combo_dict = {}
    for item in data:
        combo_key = (item["model"], item["temperature"])
        combo_dict.setdefault(combo_key, []).append((item["proportion"], item["mean"]))

    plt.figure(figsize=(8, 6))

    # Sort the combo keys by model name, then by temperature
    sorted_keys = sorted(combo_dict.keys(), key=lambda x: (x[0], x[1]))

    for (model, temp) in sorted_keys:
        values = combo_dict[(model, temp)]
        # Sort by proportion for a proper line plot
        values.sort(key=lambda x: x[0])
        x = [v[0] for v in values]
        y = [v[1] for v in values]
        label_str = f"{model} (T={temp})"
        plt.plot(x, y, marker='o', label=label_str)

    plt.title("All Combinations: Accuracy vs Proportion")
    plt.xlabel("Proportion (message pass)")
    plt.ylabel("Accuracy (mean)")
    plt.grid(True)

    # Place legend in top-left corner inside the plot
    plt.legend(loc='upper left')
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "all_combinations.png"))
    plt.close()

def plot_by_model(data):
    """
    Plots one figure per model. Each figure has lines for different temperatures,
    sorted from smallest to largest.
    x-axis = proportion, y-axis = mean.
    """
    # model_dict[model][temp] = [(proportion, mean), ...]
    model_dict = {}
    for item in data:
        model = item["model"]
        temp = item["temperature"]
        model_dict.setdefault(model, {}).setdefault(temp, []).append((item["proportion"], item["mean"]))

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for model, temp_dict in model_dict.items():
        plt.figure(figsize=(8, 6))

        # Sort temperatures from smallest to largest
        sorted_temps = sorted(temp_dict.keys())
        for temp in sorted_temps:
            values = temp_dict[temp]
            # Sort by proportion
            values.sort(key=lambda x: x[0])
            x = [v[0] for v in values]
            y = [v[1] for v in values]
            plt.plot(x, y, marker='o', label=f"T={temp}")

        plt.title(f"Model: {model} — Accuracy vs Proportion")
        plt.xlabel("Proportion (message pass)")
        plt.ylabel("Accuracy (mean)")
        plt.grid(True)
        plt.legend(loc='upper left')

        filename = f"model_{model.replace('.', '_')}.png"
        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_DIR, filename))
        plt.close()

def plot_by_temperature(data):
    """
    Plots one figure per temperature. Each figure has lines for different models,
    sorted alphabetically by model name.
    x-axis = proportion, y-axis = mean.
    """
    # temp_dict[temp][model] = [(proportion, mean), ...]
    temp_dict = {}
    for item in data:
        model = item["model"]
        temp = item["temperature"]
        temp_dict.setdefault(temp, {}).setdefault(model, []).append((item["proportion"], item["mean"]))

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Sort temperatures from smallest to largest
    for temp in sorted(temp_dict.keys()):
        model_dict = temp_dict[temp]

        plt.figure(figsize=(8, 6))

        # Sort model names alphabetically
        sorted_models = sorted(model_dict.keys())
        for model in sorted_models:
            values = model_dict[model]
            # Sort by proportion
            values.sort(key=lambda x: x[0])
            x = [v[0] for v in values]
            y = [v[1] for v in values]
            plt.plot(x, y, marker='o', label=f"{model}")

        plt.title(f"Temperature: {temp} — Accuracy vs Proportion")
        plt.xlabel("Proportion (message pass)")
        plt.ylabel("Accuracy (mean)")
        plt.grid(True)
        plt.legend(loc='upper left')

        filename = f"temp_{temp}.png"
        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_DIR, filename))
        plt.close()

def main():
    # Gather all data
    data = gather_results(RESULTS_DIR)
    if not data:
        print("No data found in results directory.")
        return

    # 1) One figure with all (model + temperature) lines
    plot_all_combinations(data)

    # 2) One figure per model, lines by temperature
    plot_by_model(data)

    # 3) One figure per temperature, lines by model
    plot_by_temperature(data)

    print("All plots generated and saved to the 'plots/' directory.")

if __name__ == "__main__":
    main()

