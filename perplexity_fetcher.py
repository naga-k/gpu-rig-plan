import requests
import json
import os
from typing import List, Dict
import logging

class PerplexityPaperFetcher:
    def __init__(self, api_key: str):
        self.api_url = "https://api.perplexity.ai/chat/completions"
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    SURFACE_RECONSTRUCTION_PAPERS = """Find PDFs of these computer graphics papers:
    - "Geometric structures for three dimensional shape representation" by Boissonnat
    - "Three-dimensional alpha shapes" by Edelsbrunner and Mücke
    - "A new Voronoi-based surface reconstruction algorithm" by Amenta, Bern, and Kamvysselis
    - "The ball-pivoting algorithm for surface reconstruction" by Bernardini
    - "The power crust, unions of balls, and the medial axis transform" by Amenta, Choi, and Kolluri
    - "Spectral surface reconstruction from noisy point clouds" by Kolluri, Shewchuk, and O'Brien"""

    RBF_PAPERS = """Find PDFs of:
    - "Reconstruction and representation of 3D objects with radial basis functions" by Carr
    - "Surface reconstruction from unorganized points" by Hoppe
    - "A volumetric method for building complex models from range images" by Curless and Levoy
    - "Point set surfaces" by Alexa
    - "Multi-Level partition of unity implicits" by Ohtake
    - "Interpolating and approximating implicit surfaces from polygon soup" by Shen, O'Brien, and Shewchuk"""

    POISSON_PAPERS = """Find PDFs of:
    - "Reconstruction of solid models from oriented point sets" by Kazhdan
    - "Gradient domain high dynamic range compression" by Fattal, Lischinski, and Werman
    - "Poisson image editing" by Pérez, Gangnet, and Blake
    - "Simulating water and smoke with an octree data structure" by Losasso, Gibou, and Fedkiw
    - "Mesh editing with Poisson-based gradient field manipulation" by Yu
    - "Charms: a simple framework for adaptive simulation" by Grinspun, Krysl, and Schröder
    - "Filling holes in complex surfaces using volumetric diffusion" by Davis
    - "Efficiently combining positions and normals for precise 3D geometry" by Nehab"""

    def search_papers(self, query: str) -> Dict:
        """Search for papers using Perplexity API"""
        payload = {
            "model": "pplx-7b-chat",
            "messages": [{
                "role": "user",
                "content": query
            }],
            "max_tokens": 1024,
            "temperature": 0.7,
            "return_citations": True,
            "search_domain_filter": ["academic"],
        }

        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.logger.error(f"API request failed: {e}")
            return {}

    def process_results(self, results: Dict, output_dir: str = "./papers"):
        """Process and save search results"""
        os.makedirs(output_dir, exist_ok=True)
        
        try:
            citations = results.get("citations", [])
            with open(os.path.join(output_dir, "search_results.json"), "w") as f:
                json.dump(citations, f, indent=2)
            self.logger.info(f"Saved {len(citations)} results")
        except Exception as e:
            self.logger.error(f"Error processing results: {e}")

    def search_all_papers(self) -> List[Dict]:
        """Search for all paper categories"""
        all_results = []
        queries = [
            ("Surface Reconstruction", self.SURFACE_RECONSTRUCTION_PAPERS),
            ("RBF Papers", self.RBF_PAPERS),
            ("Poisson Papers", self.POISSON_PAPERS)
        ]

        for category, query in queries:
            self.logger.info(f"Searching {category}...")
            results = self.search_papers(query)
            if results:
                all_results.append({
                    "category": category,
                    "results": results
                })
        return all_results

def main():
    api_key = "YOUR_PERPLEXITY_API_KEY"
    fetcher = PerplexityPaperFetcher(api_key)
    
    # Search all paper categories
    all_results = fetcher.search_all_papers()
    fetcher.process_results(all_results)

if __name__ == "__main__":
    main()