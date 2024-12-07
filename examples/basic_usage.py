from pathlib import Path
from memo_generator import MemoGenerator, FinancialData

def main():
    # Initialize generator
    generator = MemoGenerator()
    
    # Create sample financial data
    financial_data = FinancialData(
        revenue=10_000_000,
        costs=7_000_000,
        ebitda=3_000_000,
        growth_rate=25.5,
        market_size=1_000_000_000,
        competitors=["Competitor A", "Competitor B", "Competitor C"],
        key_metrics={
            "gross_margin": "30%",
            "customer_acquisition_cost": "$500",
            "lifetime_value": "$5000",
            "churn_rate": "5%",
            "arr": "$8M"
        }
    )
    
    # Generate memo
    memo = generator.generate_memo(financial_data)
    
    # Save output
    output_path = Path("output/memo.txt")
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(memo)
    print(f"Memo generated and saved to {output_path}")

if __name__ == "__main__":
    main()