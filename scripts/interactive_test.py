from keyword_sources import get_google_suggestions, get_bing_suggestions, get_youtube_suggestions
from gemini_enrichment import enrich_keywords_with_gemini
import keyword_metrics
import keyword_clustering
import my_utils
import pandas as pd
import os
from datetime import datetime


def to_df(keywords, source, seed):
    """Convert keywords list to DataFrame"""
    return pd.DataFrame({
        "keyword": keywords,
        "source": source,
        "seed": seed
    })


def update_google_sheet(df_clustered):
    """
    Update Google Sheets with the keywords
    This appends new keywords to the existing sheet
    """
    try:
        print("\n📤 Updating Google Sheet...")
        print("   ├─ This will APPEND keywords to Keyword_Clusters sheet")
        print("   └─ Note: Keywords accumulate (duplicates possible)")
        
        # For now, save to a local file that can be manually copied
        # In production, you'd use Google Sheets API here
        
        print("\n⚠️  MANUAL STEP REQUIRED:")
        print("   1. Open: data/processed/clustered_keywords.csv")
        print("   2. Select all data (Ctrl+A)")
        print("   3. Copy (Ctrl+C)")
        print("   4. Paste into Google Sheets 'Keyword_Clusters' at A2")
        print("   5. Done! ✅")
        print("\n   OR use n8n workflow for automatic updates")
        
        return True
        
    except Exception as e:
        print(f"❌ Error updating Google Sheet: {str(e)}")
        return False


def process_keyword(seed, update_sheets=False):
    """
    Main processing function for a single seed keyword
    
    Args:
        seed (str): The seed keyword to research
        update_sheets (bool): Whether to update Google Sheets
        
    Returns:
        df_clustered: DataFrame with scored and clustered keywords
        total_keywords: Total number of keywords generated
    """
    
    print(f"\n{'='*60}")
    print(f"🔍 RESEARCHING: '{seed}'")
    print(f"{'='*60}\n")
    
    try:
        # Step 1: Fetch suggestions from multiple sources
        print("📡 Step 1: Fetching suggestions from Google, Bing, YouTube...")
        print("   ├─ Google Suggestions API")
        google = to_df(get_google_suggestions(seed), "google", seed)
        print(f"   ├─ Found {len(google)} keywords from Google")
        
        print("   ├─ Bing Suggestions API")
        bing = to_df(get_bing_suggestions(seed), "bing", seed)
        print(f"   ├─ Found {len(bing)} keywords from Bing")
        
        print("   └─ YouTube Suggestions API")
        youtube = to_df(get_youtube_suggestions(seed), "youtube", seed)
        print(f"   └─ Found {len(youtube)} keywords from YouTube")
        
        # Combine and remove duplicates
        df_suggest = pd.concat([google, bing, youtube]).drop_duplicates()
        print(f"\n✅ Total unique suggestions: {len(df_suggest)} keywords\n")
        
        # Step 2: LLM Enrichment with Gemini
        print("🤖 Step 2: Enriching with Gemini AI...")
        print("   └─ Generating semantic variations...")
        gemini_keywords = enrich_keywords_with_gemini(seed, n=10)
        df_gemini = to_df(gemini_keywords, "gemini", seed)
        print(f"\n✅ Generated {len(df_gemini)} keywords from Gemini\n")
        
        # Step 3: Combine all keywords
        print("🔗 Step 3: Combining all sources...")
        df_all = pd.concat([df_suggest, df_gemini]).drop_duplicates()
        print(f"✅ Total unique keywords: {len(df_all)}\n")
        
        # Step 4: Score keywords
        print("📊 Step 4: Scoring keywords (5-factor algorithm)...")
        print("   ├─ Factor 1: Competition Score (40%)")
        print("   ├─ Factor 2: Word Count Score (25%)")
        print("   ├─ Factor 3: Source Diversity (15%)")
        print("   ├─ Factor 4: Trend Score (12%)")
        print("   └─ Factor 5: Uniqueness Score (8%)")
        df_scored = keyword_metrics.compute_keyword_scores(df_all)
        print(f"\n✅ Scoring complete\n")
        
        # Step 5: Cluster keywords
        print("🎯 Step 5: Clustering keywords...")
        print("   └─ Using K-means clustering (k=5)...")
        df_clustered = keyword_clustering.cluster_keywords(df_scored, n=5)
        print(f"✅ Clustered into 5 groups\n")
        
        # Step 6: Save results locally
        print("💾 Step 6: Saving results locally...")
        safe_seed = seed.replace(" ", "_").replace("/", "-").lower()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data/processed/{safe_seed}_{timestamp}_results.csv"
        my_utils.save_df(df_clustered, filename)
        print(f"✅ Saved to: {filename}\n")
        
        # Step 7: Optional Google Sheets update
        if update_sheets:
            print("Step 7: Updating Google Sheets...")
            # Save to clustered_keywords.csv for manual/n8n update
            my_utils.save_df(df_clustered, "data/processed/clustered_keywords.csv")
            print("✅ Updated clustered_keywords.csv")
            print("   Ready for Google Sheets (manual copy-paste or n8n automation)")
        
        return df_clustered, len(df_all)
        
    except Exception as e:
        print(f"\n❌ Error processing '{seed}': {str(e)}\n")
        return None, 0


def display_results(df_clustered, seed, total_keywords):
    """Display results in a beautiful format"""
    
    if df_clustered is None or df_clustered.empty:
        print("❌ No results to display")
        return
    
    print(f"\n{'='*60}")
    print(f"✨ TOP KEYWORDS FOR: '{seed}'")
    print(f"{'='*60}\n")
    
    # Show top 15 keywords
    print(f"{'Rank':<6} {'Keyword':<35} {'Score':<8} {'Cluster':<8}")
    print("-" * 60)
    
    for idx, (_, row) in enumerate(df_clustered.head(15).iterrows(), 1):
        keyword = row['keyword'][:33]  # Truncate long keywords
        score = row['score']
        cluster = row['cluster']
        print(f"{idx:<6} {keyword:<35} {score:<8.2f} {cluster:<8}")
    
    print("-" * 60)
    
    # Statistics
    print(f"\n📊 STATISTICS:")
    print(f"   • Total Keywords Generated: {total_keywords}")
    print(f"   • Highest Score: {df_clustered['score'].max():.2f}")
    print(f"   • Lowest Score: {df_clustered['score'].min():.2f}")
    print(f"   • Average Score: {df_clustered['score'].mean():.2f}")
    print(f"   • Clusters: {df_clustered['cluster'].max() + 1}")
    
    # Show keywords by source
    print(f"\n📡 KEYWORDS BY SOURCE:")
    source_counts = df_clustered['source'].value_counts()
    for source, count in source_counts.items():
        percentage = (count / len(df_clustered)) * 100
        print(f"   • {source.capitalize()}: {count} keywords ({percentage:.1f}%)")
    
    # Show keywords by cluster
    print(f"\n🎯 KEYWORDS BY CLUSTER:")
    for cluster in sorted(df_clustered['cluster'].unique()):
        cluster_data = df_clustered[df_clustered['cluster'] == cluster]
        top_3 = cluster_data.head(3)['keyword'].tolist()
        print(f"   • Cluster {cluster}: {len(cluster_data)} keywords")
        print(f"     Examples: {', '.join(top_3)}")
    
    print(f"\n{'='*60}\n")


def ask_update_sheets():
    """Ask user if they want to update Google Sheets"""
    print("\n" + "="*60)
    print("🔄 UPDATE GOOGLE SHEETS?")
    print("="*60)
    print("\nOptions:")
    print("  (y) YES  - Update Google Sheets (manual copy-paste or n8n)")
    print("  (n) NO   - Just save locally, don't update Sheets")
    print("  (h) HELP - Show how to update Google Sheets")
    print("\nDefault: NO (just local save)\n")
    
    while True:
        choice = input("Update Google Sheets? (y/n/h): ").strip().lower()
        
        if choice in ['y', 'yes']:
            return True
        elif choice in ['n', 'no', '']:
            return False
        elif choice in ['h', 'help']:
            print("\n" + "="*60)
            print("HOW TO UPDATE GOOGLE SHEETS:")
            print("="*60)
            print("\n📋 METHOD 1: Manual Copy-Paste (Instant)")
            print("   1. Find file: data/processed/clustered_keywords.csv")
            print("   2. Open Google Sheet: Keyword_Clusters")
            print("   3. Click cell A2 (first data row)")
            print("   4. Copy all data from CSV and paste into Sheet")
            print("   5. Done! ✅")
            
            print("\n🤖 METHOD 2: n8n Automation (Hands-off)")
            print("   1. n8n workflow is already configured")
            print("   2. Set to run daily at 9 AM")
            print("   3. Keywords automatically append to Google Sheet")
            print("   4. Get email notification daily")
            print("   5. No manual work needed!")
            
            print("\n" + "="*60 + "\n")
        else:
            print("❌ Please enter y, n, or h")


def main():
    """Main interactive loop"""
    
    print("\n" + "="*60)
    print("🔍 KEYWORD RESEARCH AI AGENT - INTERACTIVE MODE")
    print("="*60)
    print("\nAutomatically research keywords using:")
    print("  • Google, Bing, YouTube APIs (free)")
    print("  • Google Gemini LLM enrichment")
    print("  • Advanced 5-factor scoring algorithm")
    print("  • K-means clustering")
    print("\nFeatures:")
    print("  ✅ Test unlimited keywords")
    print("  ✅ Optional Google Sheets update")
    print("  ✅ Auto-save results with timestamp")
    print("  ✅ Beautiful statistics & clustering")
    print("\n" + "="*60 + "\n")
    
    session_count = 0
    
    while True:
        try:
            # Get user input
            seed = input("\n🔎 Enter a seed keyword to research (or 'quit' to exit): ").strip()
            
            # Check for exit command
            if seed.lower() in ['quit', 'exit', 'q', 'no']:
                print("\n👋 Thank you for using Keyword Research AI Agent!")
                print(f"   Researched {session_count} keyword(s) this session")
                print("   Results saved to: data/processed/")
                print("\n📝 Quick Tips:")
                print("   • Use n8n for daily automated updates to Google Sheets")
                print("   • Check data/processed/ for all results")
                print("   • Share results with your team\n")
                break
            
            # Validate input
            if not seed:
                print("❌ Please enter a keyword")
                continue
            
            if len(seed) < 2:
                print("❌ Keyword must be at least 2 characters")
                continue
            
            if len(seed) > 100:
                print("❌ Keyword is too long (max 100 characters)")
                continue
            
            # Ask if user wants to update Google Sheets
            update_sheets = ask_update_sheets()
            
            # Process the keyword
            print("\n⏳ Processing... (this may take 10-15 seconds)")
            df_clustered, total_keywords = process_keyword(seed, update_sheets=update_sheets)
            
            # Display results
            if df_clustered is not None:
                display_results(df_clustered, seed, total_keywords)
                session_count += 1
                
                if update_sheets:
                    print("✅ Results saved locally AND prepared for Google Sheets")
                    print("   📌 Next step: Copy data/processed/clustered_keywords.csv to Google Sheet")
                else:
                    print("✅ Results saved locally")
                    print("   📌 If you want to update Google Sheets later, reply 'y' next time")
                
                print("\nType another keyword to continue, or 'quit' to exit")
            else:
                print("⚠️  Could not process this keyword. Please try another.\n")
        
        except KeyboardInterrupt:
            print("\n\n⏹️  Interrupted by user")
            print(f"   Researched {session_count} keyword(s) this session")
            break
        
        except Exception as e:
            print(f"\n❌ Unexpected error: {str(e)}")
            print("   Please try another keyword\n")


if __name__ == "__main__":
    main()