#!/usr/bin/env python3

import sys
import importlib
from typing import Dict, List, Tuple, Optional


# Define required packages for this program
REQUIRED_PACKAGES = {
    "pandas": "Data manipulation and analysis",
    "numpy": "Numerical computing",
    "matplotlib": "Data visualization"
}

# Optional package (not required for basic functionality)
OPTIONAL_PACKAGES = {
    "requests": "HTTP library for fetching data"
}


def check_package(package_name: str) -> Tuple[bool, Optional[str]]:

    try:
        # Dynamically import the module
        # This is equivalent to: import pandas
        module = importlib.import_module(package_name)
        
        # Try to get version - most packages have __version__
        version = getattr(module, "__version__", "unknown")
        
        return (True, version)
    except ImportError:
        # Package is not installed
        return (False, None)


def check_all_dependencies() -> Dict[str, Dict[str, any]]:

    results = {}
    
    # Check required packages
    for package, description in REQUIRED_PACKAGES.items():
        installed, version = check_package(package)
        results[package] = {
            "installed": installed,
            "version": version,
            "required": True,
            "description": description
        }
    
    # Check optional packages
    for package, description in OPTIONAL_PACKAGES.items():
        installed, version = check_package(package)
        results[package] = {
            "installed": installed,
            "version": version,
            "required": False,
            "description": description
        }
    
    return results


def print_dependency_status(results: Dict[str, Dict[str, any]]) -> bool:

    print("LOADING STATUS: Loading programs...")
    print()
    print("Checking dependencies:")
    
    all_required_met = True
    
    for package, info in results.items():
        status = "[OK]" if info["installed"] else "[MISSING]"
        version_str = f"({info['version']})" if info["installed"] else ""
        required_str = "(required)" if info["required"] else "(optional)"
        
        print(f"  {status} {package} {version_str} - {info['description']} {required_str}")
        
        if info["required"] and not info["installed"]:
            all_required_met = False
    
    print()
    return all_required_met


def show_installation_instructions() -> None:
    print("=" * 60)
    print("MISSING DEPENDENCIES DETECTED")
    print("=" * 60)
    print()
    print("Option 1: Install with pip")
    print("-" * 40)
    print("  pip install -r requirements.txt")
    print()
    print("Option 2: Install with Poetry")
    print("-" * 40)
    print("  poetry install")
    print()
    print("Then run this program again.")
    print("=" * 60)


def analyze_matrix_data() -> None:

    # Import here (after checking dependencies are installed)
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    
    print("Analyzing Matrix data...")
    
    # Create sample "Matrix" data
    # Simulating resistance fighter performance metrics
    np.random.seed(42)  # For reproducible random numbers
    data = {
        "Fighter": [f"Agent_{i:03d}" for i in range(1, 11)],
        "Missions": np.random.randint(10, 100, 10),
        "Success_Rate": np.random.uniform(0.7, 0.99, 10),
        "Response_Time": np.random.uniform(0.1, 2.0, 10)
    }
    
    # Create DataFrame (like a table/spreadsheet in code)
    df = pd.DataFrame(data)
    
    print(f"Processing {len(df)} data points...")
    print()
    
    # Calculate statistics
    avg_missions = df["Missions"].mean()
    avg_success = df["Success_Rate"].mean()
    
    print(f"Average missions per fighter: {avg_missions:.1f}")
    print(f"Average success rate: {avg_success:.1%}")
    print()
    
    # Create visualization
    print("Generating visualization...")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Bar chart of missions
    ax1.bar(df["Fighter"], df["Missions"], color='green', alpha=0.7)
    ax1.set_xlabel("Fighter")
    ax1.set_ylabel("Missions Completed")
    ax1.set_title("Mission Count by Fighter")
    ax1.tick_params(axis='x', rotation=45)
    
    # Scatter plot of success rate vs response time
    ax2.scatter(df["Response_Time"], df["Success_Rate"], 
                s=df["Missions"]*2, alpha=0.6, color='blue')
    ax2.set_xlabel("Response Time (s)")
    ax2.set_ylabel("Success Rate")
    ax2.set_title("Performance Analysis")
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Save the plot
    output_file = "matrix_analysis.png"
    plt.savefig(output_file, dpi=100, bbox_inches='tight')
    plt.close()
    
    print()
    print("Analysis complete!")
    print(f"Results saved to: {output_file}")


def main() -> None:

    print("=" * 60)
    print("THE MATRIX - LOADING PROGRAMS")
    print("=" * 60)
    print()
    
    # Check dependencies
    results = check_all_dependencies()
    all_ok = print_dependency_status(results)
    
    if not all_ok:
        show_installation_instructions()
        sys.exit(1)
    
    print("All required dependencies loaded!")
    print()
    
    # Run analysis
    try:
        analyze_matrix_data()
    except Exception as e:
        print(f"Error during analysis: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
