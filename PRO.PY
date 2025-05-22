#WORKING CORRECT

import datetime
import random
import re
import os
import webbrowser
from typing import List, Dict, Tuple, Set, Optional
from collections import defaultdict
from IPython.display import HTML

class SmartOutfitRecommender:
    def __init__(self, wardrobe_db: List[Dict] = None):
        self.wardrobe_db = wardrobe_db if wardrobe_db else []
        self._initialize_wardrobe()
        self.recent_outfits = defaultdict(list)
        self.max_recent_outfits = 5
        self.recent_combinations = defaultdict(list)
        self.max_recent_combinations = 3
        self.color_variants = {  # Expanded color matching
            'red': ['maroon', 'burgundy', 'crimson', 'ruby','black', 'white', 'pink'],
            'blue': ['navy', 'teal', 'sky blue', 'aqua','black', 'white'],
            'green': ['olive', 'emerald', 'mint', 'forest','black', 'white'],
            'green': ['olive', 'emerald', 'mint', 'forest','black', 'white'],
            "purple": ["yellow", "mint", "white", "black", "gold", "gray",'black', 'white'],
            "pink": ["green", "brown", "white", "navy", "gray", "black"],
            "black": ["gold", "silver", "white", "red", "pink", "navy"],
            "white": ["black", "navy", "red", "gold", "green", "purple"],
            "gray": ["yellow", "pink", "white", "black", "purple", "red"],
            "brown": ["blue", "cream", "green", "white", "pink", "beige",'black'],
            "beige": ["brown", "green", "blue", "white", "navy", "black"],
            "navy": ["gold", "red", "white", "pink", "beige", "orange"],
            "cream": ["brown", "green", "navy", "black", "red", "purple"],
            "gold": ["black", "navy", "red", "purple", "green", "blue",'black', 'white'],
            "silver": ["blue", "black", "white", "red", "purple", "gray"],
            "orange": ["blue", "white", "black", "green", "navy", "brown"],
            "teal": ["coral", "white", "navy", "gold", "brown", "black"],
            "maroon": ["gold", "white", "navy", "green", "gray", "beige"],
            "peach": ["navy", "white", "mint", "gray", "green", "brown"],
            "mint": ["peach", "white", "navy", "gray", "brown", "pink"],
            "lavender": ["yellow", "white", "gray", "navy", "green", "gold",'black'],
            "olive": ["red", "white", "navy", "black", "orange", "pink"],
            "coral": ["teal", "white", "navy", "gray", "black", "gold"],
            "mustard": ["purple", "white", "navy", "black", "green", "gray"],
            "turquoise": ["coral", "white", "navy", "gold", "black", "red"],
            "charcoal": ["gold", "white", "red", "navy", "pink", "green"],
            "violet": ["yellow", "white", "gray", "navy", "gold", "green",'black'],
            "indigo": ["gold", "white", "red", "navy", "pink", "orange",'black']
        }
        self.color_weights = {
            'red': 0.9, 'blue': 0.9, 'green': 0.8, 'purple': 0.7, 
            'pink': 0.7, 'black': 1.0, 'white': 1.0, 'gray': 0.6,
            'brown': 0.5, 'beige': 0.5, 'navy': 0.8, 'cream': 0.5,
            'gold': 0.7, 'silver': 0.6, 'orange': 0.6, 'yellow': 0.5
        }

    def _initialize_wardrobe(self):
        """Ensure wardrobe items have required fields"""
        for item in self.wardrobe_db:
            if "tags" not in item:
                item["tags"] = []
            if "category" not in item:
                item["category"] = "unknown"

    def _expand_color_requirements(self, color: str) -> List[str]:
        """Expand color requirements with variants, harmonies, and linguistic variations"""
        base_color = color.lower()
        variants = self.color_variants.get(base_color, [])
        
        # Color theory expansions
        color_harmonies = {
            'red': ['crimson', 'scarlet', 'ruby', 'vermillion', 'burgundy'],
            'orange': ['coral', 'peach', 'terracotta', 'amber', 'rust'],
            'yellow': ['gold', 'mustard', 'lemon', 'maize', 'butter'],
            'green': ['emerald', 'forest', 'mint', 'olive', 'sage'],
            'blue': ['navy', 'azure', 'cerulean', 'teal', 'sapphire'],
            'purple': ['violet', 'lavender', 'amethyst', 'plum', 'orchid'],
            'pink': ['rose', 'blush', 'fuchsia', 'hotpink', 'salmon'],
            'brown': ['tan', 'chocolate', 'caramel', 'coffee', 'mocha'],
            'black': ['ebony', 'jet', 'onyx', 'charcoal', 'raven'],
            'white': ['ivory', 'cream', 'eggshell', 'snow', 'chalk'],
            'gray': ['slate', 'steel', 'pewter', 'ash', 'silver']
        }

        complementary_map = {
            'red': ['green'],
            'green': ['red'],
            'blue': ['orange'],
            'orange': ['blue'],
            'yellow': ['purple'],
            'purple': ['yellow'],
            'pink': ['mint'],
            'brown': ['teal'],
            'black': ['metallic'],
            'white': ['pastel']
        }

        analogous_map = {
            'red': ['vermillion', 'coral', 'burgundy'],
            'orange': ['amber', 'peach', 'terracotta'],
            'yellow': ['gold', 'mustard', 'chartreuse'],
            'green': ['olive', 'sage', 'emerald'],
            'blue': ['navy', 'teal', 'aqua'],
            'purple': ['lavender', 'violet', 'magenta'],
            'pink': ['rose', 'blush', 'fuchsia']
        }

        expansions = []
        expansions += color_harmonies.get(base_color, [])
        expansions += complementary_map.get(base_color, [])
        expansions += analogous_map.get(base_color, [])
        
        return list(set([base_color] + variants + expansions))

    def _expand_color_requirements_with_weights(self, color: str):
        base_color = color.lower()
        variants = self.color_variants.get(base_color, [])
        expanded = [(base_color, self.color_weights.get(base_color, 0.7))]
        for variant in variants:
            weight = self.color_weights.get(variant, 0.5) * 0.9
            expanded.append((variant, weight))
        return expanded

    def _get_color_matches(self, item: Dict, color_requirements: list) -> float:
        """Enhanced color matching with name analysis and partial matches"""
        item_colors = set()
        # Extract from tags
        item_colors.update([t.lower() for t in item.get("tags", []) if t.lower() in self.color_variants])
        
        # Extract from name using regex
        name_colors = re.findall(r'\b(' + '|'.join(self.color_variants.keys()) + r')\b', item["name"].lower())
        item_colors.update(name_colors)
        
        # Check for partial matches (e.g. "lightpink" contains "pink")
        for color in self.color_variants:
            if color in item["name"].lower().replace(' ', ''):
                item_colors.add(color)

        if not item_colors:
            return 0.0
        
        best_score = 0.0
        for color, weight in color_requirements:
            if color in item_colors:
                best_score = max(best_score, weight)
            # Check for compound color names
            elif any(color in c for c in item_colors):
                best_score = max(best_score, weight * 0.8)
                
        return best_score

    def _track_recent_items(self, items: List[Dict]):
        """Track recently used items to avoid repetition"""
        for item in items:
            category = item["category"]
            self.recent_outfits[category].append(item["id"])
            if len(self.recent_outfits[category]) > self.max_recent_outfits:
                self.recent_outfits[category].pop(0)

    def get_context(self) -> Dict:
        """Determine current time and weather context"""
        now = datetime.datetime.now()
        hour = now.hour
        month = now.month
        
        time_of_day = "morning" if 5 <= hour < 12 else "afternoon" if 12 <= hour < 17 else "evening" if 17 <= hour < 21 else "night"
        
        if month in [12, 1, 2]:
            season, weather = "winter", "cold"
        elif month in [3, 4, 5]:
            season, weather = "summer", "hot"
        elif month in [6, 7, 8, 9]:
            season, weather = "monsoon", "humid"
        else:
            season, weather = "autumn", "pleasant"
            
        return {
            "time": time_of_day,
            "weather": weather,
            "season": season,
            "needs_layer": weather in ["cold", "rainy"] or season in ["winter", "monsoon"]
        }

    def analyze_occasion(self, prompt: str):
        """Identify the occasion(s) from the prompt. Returns a list of detected occasions."""
        prompt = prompt.lower()
        # Expanded set of keywords for sporty/active occasions
        activity_occasions = {
            "swimming": ["swimming", "swim", "pool", "swimwear", "water sports"],
            "gym": ["gym", "workout", "exercise", "fitness", "training"],
            "hiking": ["hiking", "trekking", "mountain", "trail", "outdoor adventure", "climbing"],
            "trekking": ["trekking", "hiking", "mountain", "trail", "outdoor adventure", "climbing"],
            "yoga": ["yoga", "stretch", "asanas", "meditation"],
            "camping": ["camping", "camp", "tent"],
            "running": ["running", "jogging", "run"],
            "cycling": ["cycling", "biking", "bike"]
        }
        other_occasions = {
            "beach party": ["beach party", "beachparty"],
            "wedding": ["wedding", "marriage"],
            "office party": ["office party", "work party"],
            "date": ["date", "romantic"],
            "party": ["party", "celebration"],
            "interview": ["interview"],
            "business meeting": ["business meeting", "meeting"],
            "office": ["office", "work"],
            "picnic": ["picnic"],
            "shopping": ["shopping", "mall"],
            "funeral": ["funeral"],
            "ritual": ["ritual", "temple"],
            "festival": ["festival", "festive"],
            "casual": ["casual", "outing"]
        }
        detected = set()
        # First check for multi-word occasions
        for occ, keywords in other_occasions.items():
            if any(f" {kw} " in f" {prompt} " for kw in keywords):
                detected.add(occ)
        # Then check single-word matches
        for occ, keywords in {**activity_occasions, **other_occasions}.items():
            if any(kw in prompt.split() for kw in keywords):
                detected.add(occ)
        # Prioritize beach party over swimming
        if "beach party" in detected:
            detected.discard("swimming")
            return ["beach party"]
        # If any activity occasion is detected, return only that (for strong match)
        for act in activity_occasions:
            if act in detected:
                return [act]
        # --- PATCH: Office + Ethnic occasion logic ---
        office_ethnic_keywords = {"ethnic", "traditional", "ritual", "festive", "ceremony"}
        if "office" in detected:
            # If any ethnic keyword is in the prompt, return both
            for kw in office_ethnic_keywords:
                if kw in prompt:
                    return ["office", kw]
            if "party" in detected or "office party" in detected:
                return ["office party"]
            if "ritual" in detected or "festival" in detected:
                return ["office", "ritual"]
            if len(detected) > 1:
                detected.discard("office")
                return ["office"] + list(detected)
            return ["office"]
        if detected:
            return list(detected)
        return ["general"]

    def extract_requirements(self, prompt: str) -> Tuple[List[str], List[str], List[str]]:
        """Extract required, preferred and forbidden keywords from prompt"""
        prompt = prompt.lower()
        required, preferred, forbidden = [], [], []
        
        # Color extraction
        color_matches = re.findall(r'\b(?:in|wearing|color|colour|shade of|like)\s+(\w+)', prompt)
        required.extend(color_matches)
        
        # Avoid keywords
        avoid_matches = re.findall(r'\b(?:avoid|not|no|dont want|don\'t want|skip)\s+(\w+)', prompt)
        forbidden.extend(avoid_matches)
        
        # Special outfit types
        if "one piece" in prompt or "dress" in prompt or "gown" in prompt:
            required.append("one_piece")
        if "swim" in prompt or "swimming" in prompt:
            required.append("swimwear")
        
        # Layer handling (expanded keywords)
        layer_keywords = ["layer", "jacket", "blazer", "sweater", "coat", "cardigan", "overcoat", "wrap"]
        # --- PATCH: Add specific layer types to required ---
        detected_layers = [kw for kw in layer_keywords if kw in prompt]
        if any(f"no {kw}" in prompt for kw in layer_keywords):
            forbidden.append("layer")
        elif detected_layers:
            required.extend(detected_layers)  # Add specific types like "jacket", "blazer"
        elif any(kw in prompt for kw in layer_keywords):
            required.append("layer")  # Fallback to generic layer
            
        return list(set(required)), list(set(preferred)), list(set(forbidden))

    def filter_items_by_occasion(self, occasions) -> List[Dict]:
        """Filter items based on one or more occasion tags, with robust support for sporty/activewear and party logic."""
        if isinstance(occasions, str):
            occasions = [occasions]
        occasion_items = []
        sporty_tags = {
            "swimming": ["swimming", "swimwear", "pool", "quick_dry"],
            "gym": ["gym", "sporty", "workout", "exercise", "training"],
            "hiking": ["hiking", "trekking", "mountain_climbing", "camping", "climbing", "running"],
            "trekking": ["trekking", "hiking", "mountain_climbing", "camping", "climbing", "running"],
            "yoga": ["yoga"],
            "camping": ["camping"],
            "running": ["running"],
            "cycling": ["cycling", "biking"]
        }
        # --- Party/office party logic ---
        party_tags = {"party", "fancy", "elegant", "stylish"}
        for item in self.wardrobe_db:
            tags = set(item.get("tags", []))
            matched = False
            for occ in occasions:
                # Sporty/activewear
                if occ in sporty_tags:
                    if any(tag in tags for tag in sporty_tags[occ]):
                        occasion_items.append(item)
                        matched = True
                        break
                # Office party and all party types
                if occ in ["office party", "party", "beach party", "wedding", "date"]:
                    if tags & party_tags:
                        occasion_items.append(item)
                        matched = True
                        break
            if matched:
                continue
            # For other occasions, match by tag
            if any(tag in tags for tag in occasions):
                occasion_items.append(item)
            elif "casual" in occasions and "casual" in tags:
                occasion_items.append(item)
        return occasion_items

    def filter_by_requirements(self, items: List[Dict], required: List[str], forbidden: List[str]) -> List[Dict]:
        """Enhanced filtering with color priority across all categories"""
        color_reqs = [r for r in required if r in self.color_variants]
        color_variants = set()
        for color in color_reqs:
            color_variants.update(self._expand_color_requirements(color))
            
        filtered = []
        for item in items:
            tags = item.get("tags", [])
            category = item["category"]
            
            # Color requirement check
            color_match = False
            if color_reqs:
                # Check both tags and name
                item_colors = set(tags).union(
                    set(re.findall(r'\b('+'|'.join(color_variants)+r')\b', item["name"].lower()))
                )
                color_match = not color_variants.isdisjoint(item_colors)

            # Category-specific checks
            category_ok = True
            for req in required:
                if req == "one_piece" and category != "one_piece":
                    category_ok = False
                elif req == "layer" and category != "layer":
                    category_ok = False

            # Final inclusion logic
            if color_match or not color_reqs:
                filtered.append(item)
                
        return filtered

    def _build_color_priority_outfits(self, occasions, context, required, forbidden):
        """Create outfits prioritizing color-matched items"""
        color_reqs = [r for r in required if r in self.color_variants]
        if not color_reqs:
            return []
        color_variants = set()
        for color in color_reqs:
            color_variants.update(self._expand_color_requirements(color))
        # Filter items matching color and occasion
        occasion_items = self.filter_items_by_occasion(occasions)
        color_matched = [item for item in occasion_items 
                        if set(item.get("tags", [])).intersection(color_variants) or
                        any(c in item["name"].lower() for c in color_variants)]
        if not color_matched:
            return []
        # Generate outfits from color-matched items
        temp_recommender = SmartOutfitRecommender(color_matched)
        # Use the main outfit generation logic, but with color-matched wardrobe
        return temp_recommender.get_unique_outfits(occasions, context, [r for r in required if r not in color_reqs], forbidden)

    def _outfit_contains_color(self, outfit, required):
        color_reqs = [r for r in required if r in self.color_variants]
        if not color_reqs:
            return True
        color_variants = set()
        for color in color_reqs:
            color_variants.update(self._expand_color_requirements(color))
        for item in outfit.get("items", []):
            tags = set(item.get("tags", []))
            name = item.get("name", "").lower()
            if not color_variants.isdisjoint(tags) or any(c in name for c in color_variants):
                return True
        return False

    def _prioritize_color_outfits(self, outfits, required_colors):
        """Enhanced prioritization with category-based scoring"""
        color_weights = {}
        for color in required_colors:
            color_weights.update(dict(self._expand_color_requirements_with_weights(color)))

        def outfit_score(outfit):
            score = 0
            main_color_score = 0
            for item in outfit.get("items", []):
                # Name-based color extraction
                name_colors = re.findall(r'\b('+'|'.join(color_weights.keys())+r')\b', item["name"].lower())
                
                # Tag-based colors
                tag_colors = [t.lower() for t in item.get("tags", []) if t.lower() in color_weights]
                
                # Combine sources
                item_colors = set(name_colors + tag_colors)
                
                for c in item_colors:
                    if c in color_weights:
                        score += color_weights[c]
                        if c in required_colors:  # Boost for exact matches
                            score += 0.5
                            
                # Category-based scoring
                if item["category"] in ["topwear", "one_piece"]:
                    main_color_score = max(main_color_score, score * 1.5)
                elif item["category"] == "bottomwear":
                    main_color_score = max(main_color_score, score * 1.2)
                    
            return main_color_score + (score * 0.5)

        return sorted(outfits, key=outfit_score, reverse=True)

    def _generate_fallback_outfits(self, occasions, context, required):
        # Fallback: generate outfits with relaxed requirements
        return self.get_unique_outfits(occasions, context, [], [])

    def _attach_matching_layer(self, outfit_items, available_layers, required, context):
        """
        Attach a matching layer to the outfit if not already present and layers are available.
        Only attach if user requested a layer or context['needs_layer'] is True.
        """
        # Check if user requested a layer
        layer_keywords = ["layer", "jacket", "blazer", "sweater", "coat", "cardigan", "overcoat", "wrap"]
        user_requested_layer = any(kw in required for kw in layer_keywords)
        weather_requires_layer = context.get("needs_layer", False)
        if not (user_requested_layer or weather_requires_layer):
            return outfit_items
        if any(item["category"] == "layer" for item in outfit_items):
            return outfit_items
        if not available_layers:
            return outfit_items
        selected_layer = random.choice(available_layers)
        return outfit_items + [selected_layer]

    def get_unique_outfits(self, occasions, context: Dict, required: List[str], forbidden: List[str]) -> List[Dict]:
        # --- COLOR PRIORITIZATION LOGIC ---
        color_priority_outfits = self._build_color_priority_outfits(occasions, context, required, forbidden)
        if color_priority_outfits:
            return color_priority_outfits[:3]
        # --- Occasion sets moved to top for scope ---
        formal_occasions = {"office", "business meeting", "interview"}
        party_occasions = {"office party", "party", "beach party", "wedding", "date"}
        casual_occasions = {"picnic", "shopping"}
        ritual_occasions = {"ritual", "temple", "home_ritual", "ceremony", "festival"}
        # --- Existing logic ---
        occasion_items = self.filter_items_by_occasion(occasions)
        filtered_items = self.filter_by_requirements(occasion_items, required, forbidden)
        # Categorize items
        tops = [item for item in filtered_items if item["category"] == "topwear"]
        bottoms = [item for item in filtered_items if item["category"] == "bottomwear"]
        one_pieces = [item for item in filtered_items if item["category"] == "one_piece"]
        layers = [item for item in filtered_items if item["category"] == "layer"]

        outfits = []
        # --- Enhanced logic for office ethnic ceremonies/rituals ---
        office_ethnic_keywords = {"ethnic", "traditional", "ceremony", "ritual", "festive", "puja", "cultural"}
        if (
            ("office" in [o.lower() for o in occasions] or 
             "business meeting" in [o.lower() for o in occasions] or
             "office party" in [o.lower() for o in occasions]
            ) and any(
                kw in " ".join([str(o).lower() for o in occasions]) 
                for kw in office_ethnic_keywords
            )
        ):
            # Ethnic/traditional outfits
            ritual_tags = {"traditional", "ritual", "ethnic", "temple", "festival", "ceremony"}
            ritual_tops = [top for top in self.wardrobe_db if top["category"] == "topwear" and set(top.get("tags", [])) & ritual_tags]
            ritual_bottoms = [bottom for bottom in self.wardrobe_db if bottom["category"] == "bottomwear" and set(bottom.get("tags", [])) & ritual_tags]
            # Strictly formal outfits (for top+bottom combo)
            formal_tags = {"formal", "office", "professional", "business_meeting"}
            exclude_tags = {"funeral", "party", "fancy", "elegant", "stylish", "date", "chic", "semi_formal", "casual", "ethnic", "ritual", "traditional", "temple", "festival", "ceremony", "festive", "puja", "cultural"}
            def is_strictly_formal(item):
                tags = set(item.get("tags", []))
                return (
                    (tags & formal_tags)
                    and not (tags & exclude_tags)
                )
            formal_tops = [top for top in self.wardrobe_db if top["category"] == "topwear" and is_strictly_formal(top)]
            formal_bottoms = [bottom for bottom in self.wardrobe_db if bottom["category"] == "bottomwear" and is_strictly_formal(bottom)]
            outfits = []
            # Add 2 traditional outfits
            if ritual_tops and ritual_bottoms:
                # First traditional outfit
                if len(ritual_tops) > 0 and len(ritual_bottoms) > 0:
                    outfits.append({
                        "type": "ethnic_set",
                        "items": [random.choice(ritual_tops), random.choice(ritual_bottoms)],
                        "reason": "Traditional ethnic wear for office ceremony"
                    })
                # Second traditional outfit (different combination)
                if len(ritual_tops) > 1 and len(ritual_bottoms) > 1:
                    used_tops = [outfit["items"][0]["id"] for outfit in outfits if outfit["type"] == "ethnic_set"]
                    used_bottoms = [outfit["items"][1]["id"] for outfit in outfits if outfit["type"] == "ethnic_set"]
                    available_tops = [top for top in ritual_tops if top["id"] not in used_tops]
                    available_bottoms = [bottom for bottom in ritual_bottoms if bottom["id"] not in used_bottoms]
                    if available_tops and available_bottoms:
                        outfits.append({
                            "type": "ethnic_set",
                            "items": [random.choice(available_tops), random.choice(available_bottoms)],
                            "reason": "Alternative traditional outfit for office ceremony"
                        })
            # Add 1 strictly formal outfit (top+bottom)
            if formal_tops and formal_bottoms and len(outfits) < 3:
                outfits.append({
                    "type": "formal_office",
                    "items": [random.choice(formal_tops), random.choice(formal_bottoms)],
                    "reason": "Professional formal wear for office ceremony"
                })
            if outfits:
                return outfits[:3]
        # --- Funeral logic: Only use items with "funeral" tag, else strictly formal ---
        if any(occ == "funeral" for occ in [o.lower() for o in occasions]):
            funeral_tops = [item for item in self.wardrobe_db if item["category"] == "topwear" and "funeral" in item.get("tags", [])]
            funeral_bottoms = [item for item in self.wardrobe_db if item["category"] == "bottomwear" and "funeral" in item.get("tags", [])]
            outfits = []
            used_top_ids = set()
            used_bottom_ids = set()
            for _ in range(3):
                available_tops = [top for top in funeral_tops if top["id"] not in used_top_ids]
                available_bottoms = [bottom for bottom in funeral_bottoms if bottom["id"] not in used_bottom_ids]
                if not available_tops or not available_bottoms:
                    break
                top = random.choice(available_tops)
                bottom = random.choice(available_bottoms)
                used_top_ids.add(top["id"])
                used_bottom_ids.add(bottom["id"])
                outfits.append({
                    "type": "funeral",
                    "items": [top, bottom],
                    "reason": "Appropriate attire for funeral"
                })
            # If less than 3, fill with strictly formal
            if len(outfits) < 3:
                formal_tags = {"formal", "office", "professional", "business_meeting"}
                exclude_tags = {"funeral", "party", "fancy", "elegant", "stylish", "date", "chic", "semi_formal", "casual", "ethnic", "ritual", "traditional", "temple", "festival", "ceremony", "festive", "puja", "cultural"}
                def is_strictly_formal(item):
                    tags = set(item.get("tags", []))
                    return (
                        (tags & formal_tags)
                        and not (tags & exclude_tags)
                    )
                formal_tops = [top for top in self.wardrobe_db if top["category"] == "topwear" and is_strictly_formal(top)]
                formal_bottoms = [bottom for bottom in self.wardrobe_db if bottom["category"] == "bottomwear" and is_strictly_formal(bottom)]
                formal_layers = [layer for layer in self.wardrobe_db if layer["category"] == "layer" and is_strictly_formal(layer)]
                used_formal_top_ids = set([item["id"] for o in outfits for item in o["items"] if item["category"] == "topwear"])
                used_formal_bottom_ids = set([item["id"] for o in outfits for item in o["items"] if item["category"] == "bottomwear"])
                for _ in range(3 - len(outfits)):
                    available_tops = [top for top in formal_tops if top["id"] not in used_formal_top_ids]
                    available_bottoms = [bottom for bottom in formal_bottoms if bottom["id"] not in used_formal_bottom_ids]
                    if not available_tops or not available_bottoms:
                        break
                    top = random.choice(available_tops)
                    bottom = random.choice(available_bottoms)
                    used_formal_top_ids.add(top["id"])
                    used_formal_bottom_ids.add(bottom["id"])
                    outfit_items = [top, bottom]
                    outfit_items = self._attach_matching_layer(outfit_items, formal_layers, required=[], context={})
                    outfits.append({
                        "type": "top+bottom+layer" if len(outfit_items) == 3 else "top+bottom",
                        "items": outfit_items,
                        "reason": "Strictly formal attire (no ethnic/party/casual) for funeral"
                    })
            return outfits[:3]
        # --- Formal/Office/Business/Interview logic ---
        elif any(occ in formal_occasions for occ in [o.lower() for o in occasions]):
            # Only use items with "formal", "office", "professional", "business_meeting", "interview" tags
            formal_tags = {"formal", "office", "professional", "business_meeting", "interview"}
            # Exclude "funeral", "party", "fancy", "elegant", "stylish", "date", "chic", "semi_formal", "casual"
            exclude_tags = {"funeral", "party", "fancy", "elegant", "stylish", "date", "chic", "semi_formal", "casual"}
            def is_strictly_formal(item):
                tags = set(item.get("tags", []))
                return (
                    (tags & formal_tags) and 
                    not (tags & exclude_tags) and
                    (item["category"] != "one_piece")  # Exclude one_pieces for formal office
                )

            formal_tops = [top for top in self.wardrobe_db 
                          if top["category"] == "topwear" and is_strictly_formal(top)]
            formal_bottoms = [bottom for bottom in self.wardrobe_db 
                             if bottom["category"] == "bottomwear" and is_strictly_formal(bottom)]
            formal_layers = [layer for layer in self.wardrobe_db 
                            if layer["category"] == "layer" and is_strictly_formal(layer)]

            outfits = []
            used_top_ids = set()
            used_bottom_ids = set()

            for _ in range(3):
                available_tops = [top for top in formal_tops if top["id"] not in used_top_ids]
                available_bottoms = [bottom for bottom in formal_bottoms if bottom["id"] not in used_bottom_ids]
                
                if not available_tops or not available_bottoms:
                    break
                    
                top = random.choice(available_tops)
                bottom = random.choice(available_bottoms)
                used_top_ids.add(top["id"])
                used_bottom_ids.add(bottom["id"])
                
                outfit_items = [top, bottom]
                
                # STRICTLY FORMAL LAYER ATTACHMENT
                if formal_layers:
                    # Only add if not already present and we have matching formal layers
                    if not any(item["category"] == "layer" for item in outfit_items):
                        selected_layer = random.choice(formal_layers)
                        outfit_items.append(selected_layer)
                
                outfits.append({
                    "type": "top+bottom+layer" if len(outfit_items) == 3 else "top+bottom",
                    "items": outfit_items,
                    "reason": f"Formal/office outfit for {occasions}" + 
                             (" (with formal layer)" if len(outfit_items) == 3 else "")
                })

            return outfits[:3]
        # --- Party-related occasions (including office party, beach party, wedding, date) ---
        party_occasions = {"office party", "party", "beach party", "wedding", "date"}
        if any(occ in party_occasions for occ in [o.lower() for o in occasions]):
            # Updated wedding/party logic: only use items with "party", "fancy", "elegant", "stylish", "wedding" tags (NO ethnic/ritual/festive unless user requests)
            if "beach party" in [o.lower() for o in occasions]:
                party_tags = {"party", "beach_party", "fancy", "elegant", "stylish"}
            elif "wedding" in [o.lower() for o in occasions]:
                party_tags = {"party", "fancy", "elegant", "stylish", "wedding"}
            else:
                party_tags = {"party", "fancy", "elegant", "stylish"}
            # Exclude ethnic/ritual/festive unless user requests
            exclude_ethnic = not any(x in [o.lower() for o in occasions] for x in ["ethnic", "ritual", "festive"])
            def not_ethnic(item):
                if not exclude_ethnic:
                    return True
                tags = set(item["tags"])
                return not ({"ethnic", "ritual", "festive", "temple", "traditional"} & tags)
            party_one_pieces = [
                op for op in self.wardrobe_db if op["category"] == "one_piece"
                if (not {"swimming", "swimwear"}.intersection(op["tags"]))
                and (party_tags.intersection(op["tags"]))
                and not_ethnic(op)
            ]
            party_tops = [
                top for top in self.wardrobe_db if top["category"] == "topwear"
                if party_tags.intersection(top["tags"]) and not_ethnic(top)
            ]
            party_bottoms = [
                bottom for bottom in self.wardrobe_db if bottom["category"] == "bottomwear"
                if party_tags.intersection(bottom["tags"]) and not_ethnic(bottom)
            ]
            party_layers = [
                layer for layer in self.wardrobe_db if layer["category"] == "layer"
                if party_tags.intersection(layer["tags"]) and not_ethnic(layer)
            ]
            outfits = []
            # 1. Top+Bottom (+Layer if requested)
            used_top_ids = set()
            used_bottom_ids = set()
            for _ in range(2):
                available_tops = [top for top in party_tops if top["id"] not in used_top_ids]
                available_bottoms = [bottom for bottom in party_bottoms if bottom["id"] not in used_bottom_ids]
                if not available_tops or not available_bottoms:
                    break
                top = random.choice(available_tops)
                bottom = random.choice(available_bottoms)
                used_top_ids.add(top["id"])
                used_bottom_ids.add(bottom["id"])
                outfit_items = [top, bottom]
                # Attach layer if needed (universal helper)
                outfit_items = self._attach_matching_layer(outfit_items, party_layers, required, context)
                outfits.append({
                    "type": "top+bottom+layer" if len(outfit_items) == 3 else "top+bottom",
                    "items": outfit_items,
                    "reason": f"Stylish combination for {occasions}" + (" (with layer)" if len(outfit_items) == 3 else "")
                })
                self.recent_outfits["tops"].append(top["id"])
                self.recent_outfits["bottoms"].append(bottom["id"])
                if len(self.recent_outfits["tops"]) > self.max_recent_outfits:
                    self.recent_outfits["tops"].pop(0)
                if len(self.recent_outfits["bottoms"]) > self.max_recent_outfits:
                    self.recent_outfits["bottoms"].pop(0)
            # 2. One-piece (+Layer if requested)
            if party_one_pieces:
                available_one_pieces = [
                    op for op in party_one_pieces
                    if op["id"] not in self.recent_outfits.get("one_piece", [])
                ]
                if not available_one_pieces:
                    available_one_pieces = party_one_pieces
                selected_one_piece = random.choice(available_one_pieces)
                outfit_items = [selected_one_piece]
                # Attach layer if needed (universal helper)
                outfit_items = self._attach_matching_layer(outfit_items, party_layers, required, context)
                outfits.insert(0, {  # Insert one-piece as first outfit
                    "type": "one_piece+layer" if len(outfit_items) == 2 else "one_piece",
                    "items": outfit_items,
                    "reason": f"Elegant one-piece for {occasions}" + (" (with layer)" if len(outfit_items) == 2 else "")
                })
                self.recent_outfits["one_piece"].append(selected_one_piece["id"])
                if len(self.recent_outfits["one_piece"]) > self.max_recent_outfits:
                    self.recent_outfits["one_piece"].pop(0)
            # After generating the party outfits, ensure layers are attached if requested
            if any(kw in required for kw in ["layer", "blazer", "jacket"]):
                party_layers = [item for item in self.wardrobe_db 
                                if item["category"] == "layer" and 
                                ("blazer" in item["tags"] or "jacket" in item["tags"])]
                for outfit in outfits:
                    # Only add layer if not already present and we have matching layers
                    if not any(item["category"] == "layer" for item in outfit["items"]) and party_layers:
                        selected_layer = random.choice(party_layers)
                        outfit["items"].append(selected_layer)
                        outfit["type"] = outfit.get("type", "") + "+layer"
                        outfit["reason"] = outfit.get("reason", "") + " (with blazer)"
            return outfits[:3]
        # --- Existing logic ---
        occasion_items = self.filter_items_by_occasion(occasions)
        filtered_items = self.filter_by_requirements(occasion_items, required, forbidden)
        # Categorize items
        tops = [item for item in filtered_items if item["category"] == "topwear"]
        bottoms = [item for item in filtered_items if item["category"] == "bottomwear"]
        one_pieces = [item for item in filtered_items if item["category"] == "one_piece"]
        layers = [item for item in filtered_items if item["category"] == "layer"]

        outfits = []
        # --- Enhanced logic for office ethnic ceremonies/rituals ---
        office_ethnic_keywords = {"ethnic", "traditional", "ceremony", "ritual", "festive", "puja", "cultural"}
        # Check if prompt is for office + ethnic/traditional/ceremony/ritual/festive/puja/cultural
        if (
            (
                any(kw in " ".join([str(o).lower() for o in occasions]) for kw in office_ethnic_keywords)
                and (
                    "office" in [o.lower() for o in occasions]
                    or "business meeting" in [o.lower() for o in occasions]
                    or "office party" in [o.lower() for o in occasions]
                )
            )
            or (
                # fallback: if both office and ethnic/traditional/ceremony/ritual/festive/puja/cultural are present in prompt
                set([o.lower() for o in occasions]) & {"office", "business meeting", "office party"}
                and set([o.lower() for o in occasions]) & office_ethnic_keywords
            )
        ):
            ethnic_tags = {"traditional", "ritual", "ethnic", "temple", "festival", "ceremony", "festive", "cultural", "puja"}
            formal_tags = {"formal", "office", "professional", "business_meeting", "interview", "corporate"}
            # Ethnic
            ethnic_tops = [item for item in self.wardrobe_db if item["category"] == "topwear" and set(item.get("tags", [])) & ethnic_tags]
            ethnic_bottoms = [item for item in self.wardrobe_db if item["category"] == "bottomwear" and set(item.get("tags", [])) & ethnic_tags]
            ethnic_one_pieces = [item for item in self.wardrobe_db if item["category"] == "one_piece" and set(item.get("tags", [])) & ethnic_tags]
            # Formal
            formal_tops = [item for item in self.wardrobe_db if item["category"] == "topwear" and set(item.get("tags", [])) & formal_tags]
            formal_bottoms = [item for item in self.wardrobe_db if item["category"] == "bottomwear" and set(item.get("tags", [])) & formal_tags]
            outfits = []
            # Ethnic one-piece
            if ethnic_one_pieces:
                outfits.append({
                    "type": "ethnic_one_piece",
                    "items": [random.choice(ethnic_one_pieces)],
                    "reason": "Traditional ethnic one-piece for office ceremony"
                })
            # Ethnic top + bottom
            if ethnic_tops and ethnic_bottoms:
                outfits.append({
                    "type": "ethnic_set",
                    "items": [random.choice(ethnic_tops), random.choice(ethnic_bottoms)],
                    "reason": "Ethnic ensemble suitable for office rituals"
                })
            # Fusion formal
            fusion_combos = []
            if ethnic_tops and formal_bottoms:
                fusion_combos.append({
                    "type": "fusion_formal",
                    "items": [random.choice(ethnic_tops), random.choice(formal_bottoms)],
                    "reason": "Ethnic top with formal bottom for ceremonial office event"
                })
            if formal_tops and ethnic_bottoms:
                fusion_combos.append({
                    "type": "fusion_formal",
                    "items": [random.choice(formal_tops), random.choice(ethnic_bottoms)],
                    "reason": "Formal top with ethnic bottom for traditional office occasion"
                })
            if fusion_combos:
                outfits.append(random.choice(fusion_combos))
            # Pure formal
            if formal_tops and formal_bottoms:
                outfits.append({
                    "type": "corporate_formal",
                    "items": [random.choice(formal_tops), random.choice(formal_bottoms)],
                    "reason": "Professional formal wear for office ceremonies"
                })
            # Always return at least ethnic outfits if available, else fallback to formal
            if outfits:
                return outfits[:3]
        # --- Party-related occasions (including office party, beach party, wedding, date) ---
        party_occasions = {"office party", "party", "beach party", "wedding", "date"}
        casual_occasions = {"picnic", "shopping"}
        formal_occasions = {"office", "business meeting", "interview"}
        ritual_occasions = {"ritual", "temple", "home_ritual", "ceremony", "festival"}
        # --- Party logic (already present) ---
        if any(occ in party_occasions for occ in [o.lower() for o in occasions]):
            # Special handling: if prompt/occasion includes both office and ethnic/traditional/ritual/festive/ceremony, allow both formal and ethnic outfits
            office_ethnic_keywords = {"ethnic", "traditional", "ritual", "festive", "ceremony"}
            prompt_lower = " ".join([str(o).lower() for o in occasions])
            if (
                ("office" in prompt_lower or "business meeting" in prompt_lower or "interview" in prompt_lower or "office party" in prompt_lower)
                and any(kw in prompt_lower for kw in office_ethnic_keywords)
            ):
                # Combine formal and ethnic outfits
                # 1. Ethnic/traditional outfits
                ritual_tags = {"traditional", "ritual", "ethnic", "temple", "festival", "home_ritual", "ceremony"}
                ritual_tops = [top for top in self.wardrobe_db if top["category"] == "topwear" and set(top.get("tags", [])) & ritual_tags]
                ritual_bottoms = [bottom for bottom in self.wardrobe_db if bottom["category"] == "bottomwear" and set(bottom.get("tags", [])) & ritual_tags]
                ritual_layers = [layer for layer in self.wardrobe_db if layer["category"] == "layer" and set(layer.get("tags", [])) & ritual_tags]
                ritual_one_pieces = [op for op in self.wardrobe_db if op["category"] == "one_piece" and set(op.get("tags", [])) & ritual_tags]
                outfits = []
                # Prefer one-piece if available
                if ritual_one_pieces:
                    selected_one_piece = random.choice(ritual_one_pieces)
                    outfit_items = [selected_one_piece]
                    outfit_items = self._attach_matching_layer(outfit_items, ritual_layers, required, context)
                    outfits.append({
                        "type": "one_piece+layer" if len(outfit_items) == 2 else "one_piece",
                        "items": outfit_items,
                        "reason": f"Ethnic/traditional outfit for {occasions}" + (" (with layer)" if len(outfit_items) == 2 else "")
                    })
                # Otherwise, top+bottom
                used_top_ids = set()
                used_bottom_ids = set()
                for _ in range(2):
                    available_tops = [top for top in ritual_tops if top["id"] not in used_top_ids]
                    available_bottoms = [bottom for bottom in ritual_bottoms if bottom["id"] not in used_bottom_ids]
                    if not available_tops or not available_bottoms:
                        break
                    top = random.choice(available_tops)
                    bottom = random.choice(available_bottoms)
                    used_top_ids.add(top["id"])
                    used_bottom_ids.add(bottom["id"])
                    outfit_items = [top, bottom]
                    outfit_items = self._attach_matching_layer(outfit_items, ritual_layers, required, context)
                    outfits.append({
                        "type": "top+bottom+layer" if len(outfit_items) == 3 else "top+bottom",
                        "items": outfit_items,
                        "reason": f"Ethnic/traditional outfit for {occasions}" + (" (with layer)" if len(outfit_items) == 3 else "")
                    })
                # 2. Add formal outfits as well
                formal_tags = {"formal", "office", "professional", "business_meeting", "interview"}
                exclude_tags = {"funeral", "party", "fancy", "elegant", "stylish", "date", "chic", "semi_formal", "casual"}
                def is_strictly_formal(item):
                    tags = set(item.get("tags", []))
                    return (
                        (tags & formal_tags)
                        and not (tags & exclude_tags)
                    )
                formal_tops = [top for top in self.wardrobe_db if top["category"] == "topwear" and is_strictly_formal(top)]
                formal_bottoms = [bottom for bottom in self.wardrobe_db if bottom["category"] == "bottomwear" and is_strictly_formal(bottom)]
                formal_layers = [layer for layer in self.wardrobe_db if layer["category"] == "layer" and is_strictly_formal(layer)]
                used_top_ids = set()
                used_bottom_ids = set()
                for _ in range(3 - len(outfits)):
                    available_tops = [top for top in formal_tops if top["id"] not in used_top_ids]
                    available_bottoms = [bottom for bottom in formal_bottoms if bottom["id"] not in used_bottom_ids]
                    if not available_tops or not available_bottoms:
                        break
                    top = random.choice(available_tops)
                    bottom = random.choice(available_bottoms)
                    used_top_ids.add(top["id"])
                    used_bottom_ids.add(bottom["id"])
                    outfit_items = [top, bottom]
                    outfit_items = self._attach_matching_layer(outfit_items, formal_layers, required, context)
                    outfits.append({
                        "type": "top+bottom+layer" if len(outfit_items) == 3 else "top+bottom",
                        "items": outfit_items,
                        "reason": f"Formal/office outfit for {occasions}" + (" (with layer)" if len(outfit_items) == 3 else "")
                    })
                return outfits[:3]
            outfits = []
            # Updated wedding/party logic: only use items with "party", "fancy", "elegant", "stylish", "wedding" tags (NO ethnic/ritual/festive unless user requests)
            if "beach party" in [o.lower() for o in occasions]:
                party_tags = {"party", "beach_party", "fancy", "elegant", "stylish"}
            elif "wedding" in [o.lower() for o in occasions]:
                party_tags = {"party", "fancy", "elegant", "stylish", "wedding"}
            else:
                party_tags = {"party", "fancy", "elegant", "stylish"}
            # Exclude ethnic/ritual/festive unless user requests
            exclude_ethnic = not any(x in [o.lower() for o in occasions] for x in ["ethnic", "ritual", "festive"])
            def not_ethnic(item):
                if not exclude_ethnic:
                    return True
                tags = set(item["tags"])
                return not ({"ethnic", "ritual", "festive", "temple", "traditional"} & tags)
            party_one_pieces = [
                op for op in one_pieces
                if (not {"swimming", "swimwear"}.intersection(op["tags"]))
                and (party_tags.intersection(op["tags"]))
                and not_ethnic(op)
            ]
            party_tops = [
                top for top in tops
                if party_tags.intersection(top["tags"]) and not_ethnic(top)
            ]
            party_bottoms = [
                bottom for bottom in bottoms
                if party_tags.intersection(bottom["tags"]) and not_ethnic(bottom)
            ]
            party_layers = [
                layer for layer in layers
                if party_tags.intersection(layer["tags"]) and not_ethnic(layer)
            ]
            # --- OUTFIT GENERATION LOGIC WITH LAYER SUPPORT ---
            # 1. Top+Bottom (+Layer if requested)
            used_top_ids = set()
            used_bottom_ids = set()
            for _ in range(2):
                available_tops = [top for top in party_tops if top["id"] not in used_top_ids]
                available_bottoms = [bottom for bottom in party_bottoms if bottom["id"] not in used_bottom_ids]
                if not available_tops or not available_bottoms:
                    break
                top = random.choice(available_tops)
                bottom = random.choice(available_bottoms)
                used_top_ids.add(top["id"])
                used_bottom_ids.add(bottom["id"])
                outfit_items = [top, bottom]
                # Attach layer if needed (universal helper)
                outfit_items = self._attach_matching_layer(outfit_items, party_layers, required, context)
                outfits.append({
                    "type": "top+bottom+layer" if len(outfit_items) == 3 else "top+bottom",
                    "items": outfit_items,
                    "reason": f"Stylish combination for {occasions}" + (" (with layer)" if len(outfit_items) == 3 else "")
                })
                self.recent_outfits["tops"].append(top["id"])
                self.recent_outfits["bottoms"].append(bottom["id"])
                if len(self.recent_outfits["tops"]) > self.max_recent_outfits:
                    self.recent_outfits["tops"].pop(0)
                if len(self.recent_outfits["bottoms"]) > self.max_recent_outfits:
                    self.recent_outfits["bottoms"].pop(0)
            # 2. One-piece (+Layer if requested)
            if party_one_pieces:
                available_one_pieces = [
                    op for op in party_one_pieces
                    if op["id"] not in self.recent_outfits.get("one_piece", [])
                ]
                if not available_one_pieces:
                    available_one_pieces = party_one_pieces
                selected_one_piece = random.choice(available_one_pieces)
                outfit_items = [selected_one_piece]
                # Attach layer if needed (universal helper)
                outfit_items = self._attach_matching_layer(outfit_items, party_layers, required, context)
                outfits.insert(0, {  # Insert one-piece as first outfit
                    "type": "one_piece+layer" if len(outfit_items) == 2 else "one_piece",
                    "items": outfit_items,
                    "reason": f"Elegant one-piece for {occasions}" + (" (with layer)" if len(outfit_items) == 2 else "")
                })
                self.recent_outfits["one_piece"].append(selected_one_piece["id"])
                if len(self.recent_outfits["one_piece"]) > self.max_recent_outfits:
                    self.recent_outfits["one_piece"].pop(0)
            return outfits[:3]
        # --- Formal/Office/Business/Interview logic ---
        elif any(occ in formal_occasions for occ in [o.lower() for o in occasions]):
            # Only use items with "formal", "office", "professional", "business_meeting", "interview" tags
            formal_tags = {"formal", "office", "professional", "business_meeting", "interview"}
            # Exclude "funeral", "party", "fancy", "elegant", "stylish", "date", "chic", "semi_formal", "casual"
            exclude_tags = {"funeral", "party", "fancy", "elegant", "stylish", "date", "chic", "semi_formal", "casual"}
            def is_strictly_formal(item):
                tags = set(item.get("tags", []))
                return (
                    (tags & formal_tags) and 
                    not (tags & exclude_tags) and
                    (item["category"] != "one_piece")  # Exclude one_pieces for formal office
                )

            formal_tops = [top for top in self.wardrobe_db 
                          if top["category"] == "topwear" and is_strictly_formal(top)]
            formal_bottoms = [bottom for bottom in self.wardrobe_db 
                             if bottom["category"] == "bottomwear" and is_strictly_formal(bottom)]
            formal_layers = [layer for layer in self.wardrobe_db 
                            if layer["category"] == "layer" and is_strictly_formal(layer)]

            outfits = []
            used_top_ids = set()
            used_bottom_ids = set()

            for _ in range(3):
                available_tops = [top for top in formal_tops if top["id"] not in used_top_ids]
                available_bottoms = [bottom for bottom in formal_bottoms if bottom["id"] not in used_bottom_ids]
                
                if not available_tops or not available_bottoms:
                    break
                    
                top = random.choice(available_tops)
                bottom = random.choice(available_bottoms)
                used_top_ids.add(top["id"])
                used_bottom_ids.add(bottom["id"])
                
                outfit_items = [top, bottom]
                
                # STRICTLY FORMAL LAYER ATTACHMENT
                if formal_layers:
                    # Only add if not already present and we have matching formal layers
                    if not any(item["category"] == "layer" for item in outfit_items):
                        selected_layer = random.choice(formal_layers)
                        outfit_items.append(selected_layer)
                
                outfits.append({
                    "type": "top+bottom+layer" if len(outfit_items) == 3 else "top+bottom",
                    "items": outfit_items,
                    "reason": f"Formal/office outfit for {occasions}" + 
                             (" (with formal layer)" if len(outfit_items) == 3 else "")
                })

            return outfits[:3]
        # --- Ritual/Traditional logic (rituals, temple, home_ritual, ceremony, festival) ---
        elif any(occ in ritual_occasions for occ in [o.lower() for o in occasions]):
            # Only use items with "traditional", "ritual", "ethnic", "temple", "festival", "home_ritual" tags
            ritual_tags = {"traditional", "ritual", "ethnic", "temple", "festival", "home_ritual", "ceremony"}
            ritual_tops = [top for top in tops if set(top["tags"]) & ritual_tags]
            ritual_bottoms = [bottom for bottom in bottoms if set(bottom["tags"]) & ritual_tags]
            ritual_layers = [layer for layer in layers if set(layer["tags"]) & ritual_tags]
            ritual_one_pieces = [op for op in one_pieces if set(op["tags"]) & ritual_tags]
            outfits = []
            # Prefer one-piece if available
            if ritual_one_pieces:
                selected_one_piece = random.choice(ritual_one_pieces)
                outfit_items = [selected_one_piece]
                # Attach layer if needed (universal helper)
                outfit_items = self._attach_matching_layer(outfit_items, ritual_layers, required, context)
                outfits.append({
                    "type": "one_piece+layer" if len(outfit_items) == 2 else "one_piece",
                    "items": outfit_items,
                    "reason": f"Traditional/ritual outfit for {occasions}" + (" (with layer)" if len(outfit_items) == 2 else "")
                })
            # Otherwise, top+bottom
            used_top_ids = set()
            used_bottom_ids = set()
            for _ in range(2):
                available_tops = [top for top in ritual_tops if top["id"] not in used_top_ids]
                available_bottoms = [bottom for bottom in ritual_bottoms if bottom["id"] not in used_bottom_ids]
                if not available_tops or not available_bottoms:
                    break
                top = random.choice(available_tops)
                bottom = random.choice(available_bottoms)
                used_top_ids.add(top["id"])
                used_bottom_ids.add(bottom["id"])
                outfit_items = [top, bottom]
                # Attach layer if needed (universal helper)
                outfit_items = self._attach_matching_layer(outfit_items, ritual_layers, required, context)
                outfits.append({
                    "type": "top+bottom+layer" if len(outfit_items) == 3 else "top+bottom",
                    "items": outfit_items,
                    "reason": f"Traditional/ritual outfit for {occasions}" + (" (with layer)" if len(outfit_items) == 3 else "")
                })
            return outfits[:3]
        # --- Casual logic (already present) ---
        elif any(occ in casual_occasions or occ == "casual" for occ in [o.lower() for o in occasions]):
            # Use all relevant tags from wardrobe for shopping/picnic/casual
            outfits = []
            # Collect all tags that appear in shopping/picnic/casual items in the wardrobe
            wardrobe_tags = set()
            for item in tops + bottoms + layers:
                if "shopping" in item["tags"] or "picnic" in item["tags"] or "casual" in item["tags"] or "outing" in item["tags"]:
                    wardrobe_tags.update(item["tags"])
            # Always include core style tags
            style_tags = {"modern", "fusion", "casual", "stylish", "shopping", "picnic", "comfortable", "lightweight", "trendy", "cotton", "denim", "jeans", "outing"}
            all_tags = wardrobe_tags | style_tags
            # Tops: must have at least one relevant tag
            candidate_tops = [top for top in tops if all_tags & set(top["tags"])]
            # Bottoms: must have at least one relevant tag
            candidate_bottoms = [bottom for bottom in bottoms if all_tags & set(bottom["tags"])]
            # Layers: all layers that have at least one relevant tag
            candidate_layers = [layer for layer in layers if all_tags & set(layer["tags"])]
            used_top_ids = set()
            used_bottom_ids = set()
            for _ in range(3):
                available_tops = [top for top in candidate_tops if top["id"] not in used_top_ids]
                available_bottoms = [bottom for bottom in candidate_bottoms if bottom["id"] not in used_bottom_ids]
                if not available_tops or not available_bottoms:
                    break
                top = random.choice(available_tops)
                bottom = random.choice(available_bottoms)
                used_top_ids.add(top["id"])
                used_bottom_ids.add(bottom["id"])
                outfit_items = [top, bottom]
                # Attach layer if needed (universal helper)
                outfit_items = self._attach_matching_layer(outfit_items, candidate_layers, required, context)
                outfits.append({
                    "type": "top+bottom+layer" if len(outfit_items) == 3 else "top+bottom",
                    "items": outfit_items,
                    "reason": "Best wardrobe match for casual outing/shopping/picnic" + (" (with layer)" if len(outfit_items) == 3 else "")
                })
                self.recent_outfits["tops"].append(top["id"])
                self.recent_outfits["bottoms"].append(bottom["id"])
                if len(self.recent_outfits["tops"]) > self.max_recent_outfits:
                    self.recent_outfits["tops"].pop(0)
                if len(self.recent_outfits["bottoms"]) > self.max_recent_outfits:
                    self.recent_outfits["bottoms"].pop(0)
            return outfits[:3]
        # --- Swimming (only if occasion is swimming) ---
        sporty_keywords = {
            "gym": ["gym", "sporty", "workout", "exercise", "training"],
            "yoga": ["yoga"],
            "hiking": ["hiking", "trekking", "mountain_climbing", "climbing"],
            "trekking": ["trekking", "hiking", "mountain_climbing", "climbing"],
            "swimming": ["swimming", "swimwear", "pool", "quick_dry"],
            "camping": ["camping"],
            "running": ["running"],
            "cycling": ["cycling", "biking"]
        }
        for key, kw_list in sporty_keywords.items():
            if key in [o.lower() for o in occasions]:
                sport_tops = [item for item in tops if any(kw in item["tags"] for kw in kw_list)]
                sport_bottoms = [item for item in bottoms if any(kw in item["tags"] for kw in kw_list)]
                sport_layers = [item for item in layers if any(kw in item["tags"] for kw in kw_list)]
                sport_one_pieces = [item for item in one_pieces if any(kw in item["tags"] for kw in kw_list)]
                # Swimming: prefer one_piece, else top+bottom
                if key == "swimming":
                    used_ids = set()
                    for op in sport_one_pieces:
                        if op["id"] not in used_ids:
                            outfit_items = [op]
                            # Attach layer if needed (universal helper)
                            outfit_items = self._attach_matching_layer(outfit_items, sport_layers, required, context)
                            outfits.append({
                                "type": "one_piece+layer" if len(outfit_items) == 2 else "one_piece",
                                "items": outfit_items,
                                "reason": "Swimwear (one-piece) for swimming" + (" (with layer)" if len(outfit_items) == 2 else "")
                            })
                            used_ids.add(op["id"])
                            if len(outfits) == 3:
                                break
                    if len(outfits) < 3 and sport_tops and sport_bottoms:
                        combos = []
                        for t in sport_tops:
                            for b in sport_bottoms:
                                combos.append((t, b))
                        used_combo_ids = set()
                        for t, b in combos:
                            combo_key = (t["id"], b["id"])
                            if combo_key not in used_combo_ids:
                                outfit_items = [t, b]
                                # Attach layer if needed (universal helper)
                                outfit_items = self._attach_matching_layer(outfit_items, sport_layers, required, context)
                                outfits.append({
                                    "type": "top+bottom+layer" if len(outfit_items) == 3 else "top+bottom",
                                    "items": outfit_items,
                                    "reason": "Swim-appropriate separates" + (" (with layer)" if len(outfit_items) == 3 else "")
                                })
                                used_combo_ids.add(combo_key)
                                if len(outfits) == 3:
                                    break
                    return outfits[:3]
                # Other sporty activities: top+bottom combos
                combos = []
                for t in sport_tops:
                    for b in sport_bottoms:
                        combos.append((t, b))
                random.shuffle(combos)
                for t, b in combos:
                    outfit_items = [t, b]
                    # Attach layer if needed (universal helper)
                    outfit_items = self._attach_matching_layer(outfit_items, sport_layers, required, context)
                    outfits.append({
                        "type": "top+bottom+layer" if len(outfit_items) == 3 else "top+bottom",
                        "items": outfit_items,
                        "reason": f"{key.title()} outfit: {t['name']} + {b['name']}" + (" (with layer)" if len(outfit_items) == 3 else "")
                    })
                    if len(outfits) == 3:
                        break
                if outfits:
                    return outfits[:3]
        # --- Fallback ---
        # Try to add a requested layer to the fallback outfits if needed
        # --- UNIVERSAL LAYER ATTACHMENT LOGIC ---
        layer_keywords = ["layer", "jacket", "blazer", "sweater", "coat", "cardigan", "overcoat", "wrap"]
        requested_layer_types = [kw for kw in layer_keywords if kw in required]
        # PATCH: Also run this block if "layer" is in required (not just specific types)
        if requested_layer_types or "layer" in required:
            all_layers = [item for item in self.wardrobe_db if item["category"] == "layer"]
            for outfit in outfits:
                has_layer = any(item["category"] == "layer" for item in outfit["items"])
                if not has_layer:
                    matching_layers = []
                    outfit_tags = set()
                    for item in outfit["items"]:
                        outfit_tags.update(item.get("tags", []))
                    # Try to match requested type and any of the outfit's tags (especially "party")
                    if requested_layer_types:
                        matching_layers = [
                            layer for layer in all_layers
                            if any(kw in layer["tags"] for kw in requested_layer_types)
                            and (set(layer["tags"]) & outfit_tags)
                        ]
                        if not matching_layers:
                            matching_layers = [
                                layer for layer in all_layers
                                if any(kw in layer["tags"] for kw in requested_layer_types)
                            ]
                    # If only "layer" is requested, just use all layers
                    if not matching_layers and all_layers:
                        matching_layers = all_layers
                    if matching_layers:
                        selected_layer = random.choice(matching_layers)
                        outfit["items"].append(selected_layer)
                        if "type" in outfit:
                            outfit["type"] += "+layer"
                        else:
                            outfit["type"] = "with_layer"
                        if "reason" in outfit:
                            if requested_layer_types:
                                outfit["reason"] += " (with " + ", ".join(requested_layer_types) + ")"
                            else:
                                outfit["reason"] += " (with layer)"
                        else:
                            if requested_layer_types:
                                outfit["reason"] = "Includes " + ", ".join(requested_layer_types)
                            else:
                                outfit["reason"] = "Includes layer"
        return outfits[:3]

    

    def recommend_outfits(self, prompt: str) -> Dict:
        # Existing context analysis
        context = self.get_context()
        occasions = self.analyze_occasion(prompt)
        required, preferred, forbidden = self.extract_requirements(prompt)
        # Get prioritized outfits
        outfits = self.get_unique_outfits(occasions, context, required, forbidden)
        # Color-enforced fallback
        if len(outfits) < 3:
            fallbacks = self._generate_fallback_outfits(occasions, context, required)
            for outfit in fallbacks:
                if self._outfit_contains_color(outfit, required) and outfit not in outfits:
                    outfits.append(outfit)
                    if len(outfits) >= 3:
                        break
        # Final color prioritization
        prioritized = self._prioritize_color_outfits(outfits, required)[:3]
        return {
            "occasion": " & ".join(occasions),
            "outfits": prioritized,
            "context": context
        }

    def print_recommendations(self, result: Dict):
        """Print outfit recommendations in a user-friendly format"""
        print(f"\nRecommended outfits for {result['occasion'].replace('_', ' ')}:")
        print(f"Context: Time - {result['context']['time']}, Weather - {result['context']['weather']}")
        
        for i, outfit in enumerate(result["outfits"], 1):
            print(f"\nOutfit {i} ({outfit['type']}): {outfit['reason']}")
            for item in outfit["items"]:
                print(f"  - {item['name']} ({item['category']})")
                print(f"    Tags: {', '.join(item['tags'])}")

    def generate_outfit_html(self, outfits, filename="outfits.html"):
        html = [
            "<!DOCTYPE html>",
            "<html><head>",
            "<title>Outfit Recommendations</title>",
            "<style>",
            "body { font-family: Arial, sans-serif; padding: 20px; }",
            ".outfit { border: 1px solid #ddd; padding: 15px; margin-bottom: 20px; }",
            ".outfit-details { margin-bottom: 10px; }",
            ".side-info { margin-bottom: 10px; }",
            ".vertical-stack { display: flex; flex-direction: row; gap: 20px; }",
            ".item { text-align: center; }",
            ".item img { width: 120px; height: 120px; object-fit: contain; border: 1px solid #ccc; margin-bottom: 5px; }",
            "</style>",
            "</head><body>",
            "<h1>Outfit Recommendations</h1>"
        ]
        for idx, outfit in enumerate(outfits, 1):
            html.append('<div class="outfit">')
            html.append('<div class="outfit-details">')
            html.append(f'<h2>Outfit {idx}</h2>')
            html.append(f'<div class="side-info">')
            for item in outfit["items"]:
                html.append(
                    f'<div><b>{item["name"]}</b> ({item["category"]})<br>'
                    f'ID: {item["id"]}<br>'
                    f'Tags: {", ".join(item["tags"])}'
                    f'</div>'
                )
            html.append('</div></div>')
            html.append('<div class="vertical-stack">')
            for item in outfit["items"]:
                html.append(
                    f'<div class="item">'
                    f'<img src="static/{item.get("image", "")}" alt="{item["name"]}"><br>'
                    f'{item["name"]}'
                    f'</div>'
                )
            html.append('</div></div></div>')
        html.append("</body></html>")
        with open(filename, "w", encoding="utf-8") as f:
            f.write("\n".join(html))
        return os.path.abspath(filename)


wardrobe_db =  [
            
            {"id": "DRSM09001", "name": "picnic_top1", "category": "topwear", "tags": ["picnic", "casual", "comfortable", "lightweight", "cotton", "red","sleeve_less"], "image": "DRSM09001.jpeg"},
            {"id": "DRSM09002", "name": "picnic_top2", "category": "topwear", "tags": ["picnic", "casual", "comfortable", "cotton", "white"], "image": "DRSM09002.jpeg"},
            {"id": "DRSM09003", "name": "casual_bottom1", "category": "bottomwear", "tags": ["casual", "comfortable", "cotton", "blue","shorts"], "image": "DRSM09003.jpeg"},
            {"id": "DRSM09004", "name": "picnic_bottom2", "category": "bottomwear", "tags": ["picnic", "casual", "comfortable", "linen", "black"], "image": "DRSM09004.jpeg"},
            {"id": "DRSM09005", "name": "picnic_layer1", "category": "layer", "tags": ["picnic", "casual", "sweater", "white","layer"], "image": "DRSM09005.jpeg"},
            {"id": "DRSM09006", "name": "hiking_top1", "category": "topwear", "tags": ["hiking", "durable", "cotton", "green","comfortable","breathable"], "image": "DRSM09006.jpeg"},
            {"id": "DRSM09007", "name": "hiking_top2", "category": "topwear", "tags": ["hiking", "durable", "breathable", "white","yoga","sleeve_less"], "image": "DRSM09007.jpeg"},
            {"id": "DRSM09008", "name": "hiking_bottom1", "category": "bottomwear", "tags": ["hiking", "durable", "comfortable", "cream","white"], "image": "DRSM09008.jpeg"},
            {"id": "DRSM09009", "name": "hiking_bottom2", "category": "bottomwear", "tags": ["hiking", "durable", "comfortable", "black","grey"], "image": "DRSM09009.jpeg"},
            {"id": "DRSM09010", "name": "hiking_layer1", "category": "layer", "tags": ["hiking", "layered", "jacket", "black","rainy","layer"], "image": "DRSM09010.jpeg"},
            {"id": "DRSM09011", "name": "camping_top1", "category": "topwear", "tags": ["camping", "durable", "cotton", "blue","aquamarine","comfortable","half-sleeve","yoga"], "image": "DRSM09011.jpeg"},
            {"id": "DRSM09012", "name": "camping_bottom1", "category": "bottomwear", "tags": ["camping", "comfortable", "cotton", "black","yoga"], "image": "DRSM09012.jpeg"},
            {"id": "DRSM09013", "name": "picnic_top1", "category": "topwear", "tags": ["picnic", "casual", "comfortable", "lightweight", "purple","violet","lavender"], "image": "DRSM09013.jpeg"},
            {"id": "DRSM09014", "name": "shopping_top2", "category": "topwear", "tags": ["shopping", "casual", "comfortable", "cotton", "brown","cream"], "image": "DRSM09014.jpeg"},
            {"id": "DRSM09015", "name": "shopping_picnic_bottom1", "category": "bottomwear", "tags": ["shopping", "casual", "comfortable", "denim", "blue","dark-blue","jeans","picnic"], "image": "DRSM09015.jpeg"},
            {"id": "DRSM09016", "name": "shopping__picnic_bottom2", "category": "bottomwear", "tags": ["shopping", "casual", "comfortable", "linen", "white","cotton","jeans","picnic"], "image": "DRSM09016.jpeg"},
            {"id": "DRSM09017", "name": "funeral_top1", "category": "topwear", "tags": ["funeral", "formal", "modest", "cotton", "black"], "image": "DRSM09017.jpeg"},
            {"id": "DRSM09018", "name": "funeral_bottom1", "category": "bottomwear", "tags": ["funeral", "formal", "modest", "cotton", "black"], "image": "DRSM09018.jpeg"},
            {"id": "DRSM09019", "name": "ritual_top1", "category": "topwear", "tags": ["temple","ritual", "traditional", "modest", "cotton", "green","pine-green","festival","festive"], "image": "DRSM09019.jpeg"},
            {"id": "DRSM09020", "name": "ritual_bottom1", "category": "bottomwear", "tags": ["temple","ritual", "traditional", "modest", "cotton", "cream","white","festival","festive"], "image": "DRSM09020.jpeg"},
            {"id": "DRSM09021", "name": "temple_visit_top1", "category": "topwear", "tags": ["temple", "traditional", "modest", "cotton", "pink"], "image": "DRSM09021.jpeg"},
            {"id": "DRSM09022", "name": "temple_visit_bottom1", "category": "bottomwear", "tags": ["temple", "traditional", "modest", "cotton", "black","navy","blue"], "image": "DRSM09022.jpeg"},
            {"id": "DRSM09023", "name": "business_meeting_top1", "category": "topwear", "tags": ["business_meeting", "formal", "office", "professional", "cotton", "black"], "image": "DRSM09023.jpeg"},
            {"id": "DRSM09024", "name": "business_meeting_bottom1", "category": "bottomwear", "tags": ["business_meeting", "formal", "office", "professional", "grey","interview"], "image": "DRSM09024.jpeg"},
            {"id": "DRSM09025", "name": "interview_top1", "category": "topwear", "tags": ["interview", "formal", "cotton", "red","business_meeting"], "image": "DRSM09025.jpeg"},
            {"id": "DRSM09026", "name": "interview_bottom1", "category": "bottomwear", "tags": ["interview", "formal", "cotton", "white","business_meeting"], "image": "DRSM09026.jpeg"},
            {"id": "DRSM09027", "name": "interview_specific_top1", "category": "topwear", "tags": ["interview", "formal", "cotton", "white","business_meeting"], "image": "DRSM09027.jpeg"},
            {"id": "DRSM09028", "name": "interview_specific_bottom1", "category": "bottomwear", "tags": ["interview", "formal", "black","business_meeting"], "image": "DRSM09028.jpeg"},
            {"id": "DRSM09029", "name": "interview_specific_layer1", "category": "layer", "tags": ["interview", "formal", "blazer", "black""business_meeting"], "image": "DRSM09029.jpeg"},
            {"id": "DRSM09030", "name": "formal_office_top1", "category": "topwear", "tags": ["formal", "office", "cotton", "grey","brown","interview","business_meeting"], "image": "DRSM09030.jpeg"},
            {"id": "DRSM09031", "name": "formal_office_top2", "category": "topwear", "tags": ["formal", "office", "linen", "orange","pink","interview","business_meeting"], "image": "DRSM09031.jpeg"},
            {"id": "DRSM09032", "name": "formal_office_bottom1", "category": "bottomwear", "tags": ["formal", "office", "cotton", "white","interview","business_meeting"], "image": "DRSM09032.jpeg"},
            {"id": "DRSM09033", "name": "formal_office_bottom2", "category": "bottomwear", "tags": ["formal", "office", "cotton", "black","interview","business_meeting"], "image": "DRSM09033.jpeg"},
            {"id": "DRSM09034", "name": "formal_office_layer1", "category": "layer", "tags": ["formal", "office", "blazer", "black","interview","business_meeting"], "image": "DRSM09034.jpeg"},
            {"id": "DRSM09035", "name": "formal_office_layer2", "category": "layer", "tags": ["formal", "office", "blazer", "white","interview","business_meeting"], "image": "DRSM09035.jpeg"},
            {"id": "DRSM09036", "name": "semi_formal_top1", "category": "topwear", "tags": ["semi_formal", "party","date", "cotton", "blue","red","sleeveless"], "image": "DRSM09036.jpeg"},
            
            {"id": "DRSM09037", "name": "semi_formal_top2", "category": "topwear", "tags": ["semi_formal", "party","date", "cotton", "green","olive_green","sleeveless"], "image": "DRSM09037.jpeg"},
            {"id": "DRSM09038", "name": "semi_formal_bottom1", "category": "bottomwear", "tags": ["semi_formal", "stylish", "cotton", "white","party","date","wedding"], "image": "DRSM09038.jpeg"},
            {"id": "DRSM09039", "name": "semi_formal_layer1", "category": "layer", "tags": ["semi_formal", "party","date", "jacket", "black","blazer"], "image": "DRSM09039.jpeg"},
            {"id": "DRSM09040", "name": "fusion_formal_top1", "category": "topwear", "tags": ["fusion", "date", "modern", "cotton", "white","black"], "image": "DRSM09040.jpeg"},
            {"id": "DRSM09041", "name": "fusion_formal_bottom1", "category": "bottomwear", "tags": ["fusion", "date", "modern", "linen", "black","party"], "image": "DRSM09041.jpeg"},
            {"id": "DRSM09042", "name": "fusion_formal_layer1", "category": "layer", "tags": ["business_meeting","formal","office", "modern", "jacket", "brown","blazer","layer"], "image": "DRSM09042.jpeg"},
            {"id": "DRSM09043", "name": "party_top1", "category": "topwear", "tags": ["party", "stylish", "cotton", "green","dark_green","date","fancy","date"], "image": "DRSM09043.jpeg"},
            {"id": "DRSM09044", "name": "party_top2", "category": "topwear", "tags": ["party", "trendy", "fancy", "blue","silk","satin","date","stylish","date"], "image": "DRSM09044.jpeg"},
            {"id": "DRSM09045", "name": "party_bottom1", "category": "bottomwear", "tags": ["party", "trendy", "silk","cotton", "blue","stylish","fancy","date"], "image": "DRSM09045.jpeg"},
            {"id": "DRSM09046", "name": "party_bottom2", "category": "bottomwear", "tags": ["party", "stylish", "silk","cotton", "brown","fancy","date"], "image": "DRSM09046.jpeg"},
            {"id": "DRSM09047", "name": "party_bottom3", "category": "bottomwear", "tags": ["party", "stylish", "silk","cotton", "black","fancy","date"], "image": "DRSM09047.jpeg"},
            {"id": "DRSM09048", "name": "party_bottom4", "category": "bottomwear", "tags": ["party", "stylish", "silk","cotton", "white","fancy","date"], "image": "DRSM09048.jpeg"},
            {"id": "DRSM09049", "name": "officee_layer1", "category": "layer", "tags": ["office", "blazer","wool", "black","formal","business_meeting","interview"], "image": "DRSM09049.jpeg"},
            {"id": "DRSM09050", "name": "party_layer2", "category": "layer", "tags": ["party", "elegant", "pink","blazer","wool","stylish","fancy"], "image": "DRSM09050.jpeg"},
            {"id": "DRSM09051", "name": "_party_top1", "category": "topwear", "tags": [ "party", "stylish", "silk", "lavender","violet","purple","cotton","date","wedding"], "image": "DRSM09051.jpeg"},
            {"id": "DRSM09052", "name": "_party_top2", "category": "topwear", "tags": ["party", "office", "trendy", "silk","cotton", "red","date","wedding"], "image": "DRSM09052.jpeg"},
            {"id": "DRSM09053", "name": "_party_bottom1", "category": "bottomwear", "tags": ["party", "date", "trendy", "silk","cotton", "red"], "image": "DRSM09053.jpeg"},
            {"id": "DRSM09054", "name": "_party_bottom2", "category": "bottomwear", "tags": ["party", "date", "stylish", "silk","cotton", "pink"], "image": "DRSM09054.jpeg"},
            {"id": "DRSM09055", "name": "_party_layer1", "category": "layer", "tags": ["party", "wedding", "blazer","wool","cotton", "white"], "image": "DRSM09055.jpeg"},
            {"id": "DRSM09056", "name": "office__layer2", "category": "layer", "tags": [ "office", "formal", "brown","blazer","cotton","wool"], "image": "DRSM09056.jpeg"},
            {"id": "DRSM09057", "name": "formal_one_piece1", "category": "one_piece", "tags": ["office_party", "formal", "stylish", "silk", "blue", "one_piece"], "image": "DRSM09057.jpeg"},
            {"id": "DRSM09058", "name": "wedding_one_piece2", "category": "one_piece", "tags": ["wedding", "elegant", "embroidered", "white", "one_piece","synthetic","stylish","fancy"], "image": "DRSM09058.jpeg"},
            {"id": "DRSM09059", "name": "wedding__top1", "category": "topwear", "tags": ["wedding", "party", "silk", "black","netted","breathable"], "image": "DRSM09059.jpeg"},
            {"id": "DRSM09060", "name": "wedding__bottom1", "category": "bottomwear", "tags": ["wedding", "party", "cotton", "black","date"], "image": "DRSM09060.jpeg"},
            {"id": "DRSM09061", "name": "wedding_formal_layer1", "category": "layer", "tags": ["wedding", "party", "blazer", "white","date"], "image": "DRSM09061.jpeg"},
            {"id": "DRSM09062", "name": "wedding_stylish_top1", "category": "topwear", "tags": ["wedding", "stylish", "embroidered", "white","party"], "image": "DRSM09062.jpeg"},
            {"id": "DRSM09063", "name": "wedding_stylish_bottom1", "category": "bottomwear", "tags": ["wedding", "stylish", "silk", "white","cotton","party","date"], "image": "DRSM09063.jpeg"},
            {"id": "DRSM09064", "name": "wedding_stylish_layer1", "category": "layer", "tags": ["wedding", "stylish", "blazer", "black","party","date"], "image": "DRSM09064.jpeg"},
            {"id": "DRSM09065", "name": "ethnic_festive_top1", "category": "topwear", "tags": ["festive", "ethnic", "embroidered", "blue","cotton","silk","traditional","festival","ritual","home_ritual","temple"], "image": "DRSM09065.jpeg"},
            {"id": "DRSM09066", "name": "ethnic_festive_bottom1", "category": "bottomwear", "tags": ["festive", "ethnic", "silk", "gold","cream","white","cotton","traditional","festival","ritual","home_ritual","temple"], "image": "DRSM09066.jpeg"},
            {"id": "DRSM09067", "name": "ethnic_festive_layer1", "category": "layer", "tags": ["festive", "ethnic", "long", "black","traditional","festival","ritual","home_ritual","temple"], "image": "DRSM09067.jpeg"},
            {"id": "DRSM09068", "name": "fusion_top1", "category": "topwear", "tags": ["ethnic", "festive", "cotton", "red","traditional","festival","ritual","home_ritual","temple"], "image": "DRSM09068.jpeg"},
            {"id": "DRSM09069", "name": "fusion_bottom1", "category": "bottomwear", "tags": ["fusion", "modern", "linen", "black","cotton","party"], "image": "DRSM09069.jpeg"},
            {"id": "DRSM09070", "name": "fusion_layer1", "category": "layer", "tags": ["fusion", "modern", "blazer", "black","party"], "image": "DRSM09070.jpeg"},
            {"id": "DRSM09071", "name": "date_night_top1", "category": "topwear", "tags": ["date_night", "stylish", "silk", "black","date"], "image": "DRSM09071.jpeg"},
            {"id": "DRSM09072", "name": "date_night_bottom1", "category": "bottomwear", "tags": ["date_night", "trendy", "jeans", "blue","cotton","date"], "image": "DRSM09072.jpeg"},
            {"id": "DRSM09073", "name": "date_night_layer1", "category": "layer", "tags": ["date_night", "wool","cotton","blazer", "black","date"], "image": "DRSM09073.jpeg"},
            {"id": "DRSM09074", "name": "rooftop_party_top1", "category": "topwear", "tags": ["rooftop", "party", "stylish", "silk", "green","cotton","date"], "image": "DRSM09074.jpeg"},
            {"id": "DRSM09075", "name": "rooftop_party_bottom1", "category": "bottomwear", "tags": ["festive", "ethnic", "silk","cream","white","cotton","traditional","festival","ritual","home_ritual","temple"], "image": "DRSM09075.jpeg"},
            {"id": "DRSM09076", "name": "rooftop_party_layer1", "category": "layer", "tags": ["rooftop", "party", "cotton","blazer", "brown"], "image": "DRSM09076.jpeg"},
            {"id": "DRSM09077", "name": "home_ritual_top1", "category": "topwear", "tags": ["home_ritual", "traditional", "cotton", "blue","silk","traditional","festival","ritual","temple","ethnic"], "image": "DRSM09077.jpeg"},
            {"id": "DRSM09078", "name": "home_ritual_bottom1", "category": "bottomwear", "tags": ["home_ritual", "cotton", "white","cream","silk","traditional","festival","ritual","temple","ethnic"], "image": "DRSM09078.jpeg"},
            {"id": "DRSM09079", "name": "home_ritual_layer1", "category": "layer", "tags": ["home_ritual",  "embroidered", "white","long","traditional","festival","ritual","temple","ethnic"], "image": "DRSM09079.jpeg"},
            {"id": "DRSM09080", "name": "versatile__top1", "category": "topwear", "tags": ["silk", "party", "fancy", "cotton", "blue","sleeveless","stylish"], "image": "DRSM09080.jpeg"},
            {"id": "DRSM09081", "name": "versatile__top2", "category": "topwear", "tags": ["cotton", "party", "fancy", "silk", "white","stylish"], "image": "DRSM09081.jpeg"},
            {"id": "DRSM09082", "name": "versatile_formal_bottom1", "category": "bottomwear", "tags": ["party", "fancy", "denim", "jeans", "blue"], "image": "DRSM09082.jpeg"},
            {"id": "DRSM09083", "name": "versatile_formal_bottom2", "category": "bottomwear", "tags": ["fancy", "party", "cotton", "black"], "image": "DRSM09083.jpeg"},
            {"id": "DRSM09084", "name": "versatile_formal_layer1", "category": "layer", "tags": ["elegant", "fancy", "party", "blazer", "black"], "image": "DRSM09084.jpeg"},
            {"id": "DRSM09085", "name": "versatile_formal_layer2", "category": "layer", "tags": ["elegant", "fancy", "party", "blazer", "brown"], "image": "DRSM09085.jpeg"},
            {"id": "DRSM09086", "name": "casual_top1", "category": "topwear", "tags": ["casual", "cotton", "lightweight", "white","picnic","shopping"], "image": "DRSM09086.jpeg"},
            {"id": "DRSM09087", "name": "casual_top2", "category": "topwear", "tags": ["casual", "cotton", "half_sleeve", "yellow","picnic","shopping"], "image": "DRSM09087.jpeg"},
            {"id": "DRSM09088", "name": "formal_bottom1142", "category": "bottomwear", "tags": ["formal", "black", "office","interview","business_meeting","cotton"], "image": "DRSM09088.jpeg"},
            {"id": "DRSM09089", "name": "casual_bottom2", "category": "bottomwear", "tags": ["casual", "cotton", "blue","denim","picnic","shopping"], "image": "DRSM09089.jpeg"},
            {"id": "DRSM09090", "name": "casual_layer1", "category": "layer", "tags": ["casual", "jacket", "pink","white","cream","picnic","shopping"], "image": "DRSM09090.jpeg"},
            {"id": "DRSM09091", "name": "gym_top1", "category": "topwear", "tags": ["gym", "sporty", "breathable", "white","yoga","hiking","camping","trekking","mountain_climbing","running","comfortable"], "image": "DRSM09091.jpeg"},
            {"id": "DRSM09092", "name": "gym_bottom1", "category": "bottomwear", "tags": ["gym", "stretchable", "comfortable", "black","yoga","hiking","camping","trekking","mountain_climbing","running"], "image": "DRSM09092.jpeg"},
            {"id": "DRSM09093", "name": "beach_top1", "category": "topwear", "tags": ["picnic","yellow","casual","shopping","cotton"], "image": "DRSM09093.jpeg"},
            {"id": "DRSM09094", "name": "beach_bottom1", "category": "bottomwear", "tags": ["picnic","yellow","casual","shopping","cotton"], "image": "DRSM09094.jpeg"},
            {"id": "DRSM09095", "name": "swimwear1", "category": "one_piece", "tags": ["swimming", "quick_dry", "blue", "one_piece"], "image": "DRSM09095.jpeg"},
            {"id": "DRSM09096", "name": "rainy_layer1", "category": "layer", "tags": ["rainy", "quick_dry", "jacket", "black","waterproof"], "image": "DRSM09096.jpeg"},
            {"id": "DRSM09097", "name": "simple_bottom1", "category": "bottomwear", "tags": ["casual","shopping","picnic","denim","outing"], "image": "DRSM09097.jpeg"},
            {"id": "DRSM09098", "name": "winter_layer1", "category": "layer", "tags": ["winter", "warm", "wool", "brown"], "image": "DRSM09098.jpeg"},
            {"id": "DRSM09099", "name": "_bottom1_", "category": "bottomwear", "tags": ["casual", "picnic", "cotton", "brown","shopping","denim"], "image": "DRSM09099.jpeg"},
            {"id": "DRSM09100", "name": "mountain_climbing_top1", "category": "topwear", "tags": ["mountain_climbing", "durable", "cotton", "green","yoga","hiking","camping","trekking","running"], "image": "DRSM09100.jpeg"},
            {"id": "DRSM09101", "name": "mountain_climbing_bottom1", "category": "bottomwear", "tags": ["mountain_climbing", "durable", "comfortable", "green","teal","yoga","hiking","camping","trekking","running"], "image": "DRSM09101.jpeg"},
            {"id": "DRSM09102", "name": "date_top1", "category": "topwear", "tags": ["date", "stylish", "chic", "casual", "pink"], "image": "DRSM09102.jpeg"},
            {"id": "DRSM09103", "name": "date_bottom1", "category": "bottomwear", "tags": ["date", "chic", "casual", "black","jeans","picnic"], "image": "DRSM09103.jpeg"},
            {"id": "DRSM09104", "name": "beach_party_one_piece1", "category": "one_piece", "tags": ["beach_party","airy", "lightweight", "pink", "one_piece"], "image": "DRSM09104.jpeg"},
            {"id": "DRSM09105", "name": "beach_party_one_piece2", "category": "one_piece", "tags": ["beach_party","airy", "lightweight", "yellow", "one_piece"], "image": "DRSM09105.jpeg"},
            {"id": "DRSM09106", "name": "__party_top1", "category": "topwear", "tags": ["party", "date", "airy", "lightweight", "pink"], "image": "DRSM09106.jpeg"},
            {"id": "DRSM09107", "name": "beach_party_bottom1", "category": "bottomwear", "tags": ["festive", "ethnic", "silk","cream","white","cotton","traditional","festival","ritual","home_ritual","temple"], "image": "DRSM09107.jpeg"},
            {"id": "DRSM09108", "name": "kurti1", "category": "topwear", "tags": ["ritual", "ethnic", "elegant", "pink", "silk", "cotton","temple","festive","traditional","festival","home_ritual"], "image": "DRSM09108.jpeg"},
            {"id": "DRSM09109", "name": "kurti2", "category": "topwear", "tags": ["ritual", "ethnic", "elegant", "green", "silk", "cotton","temple","festive","traditional","festival","home_ritual"], "image": "DRSM09109.jpeg"},
            {"id": "DRSM09110", "name": "kurti3", "category": "topwear", "tags": ["ritual", "ethnic", "elegant", "grey", "silk", "cotton","temple","festive","traditional","festival","home_ritual"], "image": "DRSM09110.jpeg"},
            {"id": "DRSM09111", "name": "swim_wear_2", "category": "one_piece", "tags": ["swimming", "quick_dry", "purple","violet","dark", "one_piece"], "image": "DRSM09111.jpeg"},
            {"id": "DRSM09112", "name": "swim_wear_3", "category": "one_piece", "tags": ["swimming", "quick_dry", "red","maroon","dark", "one_piece"], "image": "DRSM09112.jpeg"},
            {"id": "DRSM09113", "name": "casual1", "category": "topwear", "tags": ["casual", "top", "shopping", "outing", "white","cream","cotton"], "image": "DRSM09113.jpeg"},
            {"id": "DRSM09114", "name": "casual2", "category": "topwear", "tags": ["casual", "top", "shopping", "outing", "green","fullsleeves","cotton"], "image": "DRSM09114.jpeg"},
            {"id": "DRSM09115", "name": "casual3", "category": "topwear", "tags": ["casual", "top", "shopping", "outing", "white","cream","cotton","brown","fancy","picnic"], "image": "DRSM09115.jpeg"},
            {"id": "DRSM09116", "name": "casual4", "category": "topwear", "tags": ["casual", "top", "shopping", "outing", "red","cotton","fancy","picnic"], "image": "DRSM09116.jpeg"},
            {"id": "DRSM09117", "name": "casual5", "category": "topwear", "tags": ["casual", "top", "shopping", "outing","cotton","pink","fancy","picnic"], "image": "DRSM09117.jpeg"},
            {"id": "DRSM09118", "name": "jeans1", "category": "bottomwear", "tags": ["casual", "bottom", "shopping", "outing", "denim","jeans","wide","cotton","blue","dark","fancy","picnic"], "image": "DRSM09118.jpeg"},
            {"id": "DRSM09119", "name": "jeans2", "category": "bottomwear", "tags": ["casual", "bottom", "shopping", "outing", "leather","jeans","wide","black","dark","fancy","picnic","party"], "image": "DRSM09119.jpeg"},
            {"id": "DRSM09120", "name": "jeans3", "category": "bottomwear", "tags": ["casual", "bottom", "shopping", "outing", "cotton","denim","jeans","wide","white","cream","fancy","picnic","party"], "image": "DRSM09120.jpeg"},
            {"id": "DRSM09121", "name": "jeans4", "category": "bottomwear", "tags": ["casual", "bottom", "shopping", "outing", "cotton","jeans","wide","red","dark","fancy","picnic","party"], "image": "DRSM09121.jpeg"},
            {"id": "DRSM09122", "name": "jeans5", "category": "bottomwear", "tags": ["casual", "bottom", "shopping", "outing", "cotton","denim","jeans","wide","white","fancy","picnic","party"], "image": "DRSM09122.jpeg"},
            {"id": "DRSM09123", "name": "jeans6", "category": "bottomwear", "tags": ["casual", "bottom", "shopping", "outing", "leather","denim","jeans","wide","brown","fancy","picnic","party"], "image": "DRSM09123.jpeg"},
            {"id": "DRSM09124", "name": "pants1", "category": "bottomwear", "tags": ["hiking", "durable", "cotton", "grey","black","climbing","mountain","mountain_climbing","camping","comfortable","trekking","yoga","gym"], "image": "DRSM09124.jpeg"},
            {"id": "DRSM09125", "name": "pants2", "category": "bottomwear", "tags": ["hiking", "durable", "cotton", "green","olive","climbing","mountain","mountain_climbing","camping","comfortable","trekking","yoga","gym"], "image": "DRSM09125.jpeg"},
            {"id": "DRSM09126", "name": "casual6", "category": "topwear", "tags": ["casual", "top", "blue","comfortable","cotton","market"], "image": "DRSM09126.jpeg"},
            {"id": "DRSM09127", "name": "casual7", "category": "topwear", "tags": ["casual", "top", "pink","comfortable","cotton","market"], "image": "DRSM09127.jpeg"},
            {"id": "DRSM09128", "name": "topwear1", "category": "topwear", "tags": ["party", "fancy", "elegant", "silk", "cotton","green","olive","date"], "image": "DRSM09128.jpeg"},
            {"id": "DRSM09129", "name": "topwear26", "category": "topwear", "tags": ["party", "fancy", "elegant", "silk", "cotton","green","light","date"], "image": "DRSM09129.jpeg"},
            {"id": "DRSM09130", "name": "topwear2", "category": "topwear", "tags": ["party", "fancy", "elegant", "silk", "cotton","pink","light","date"], "image": "DRSM09130.jpeg"},
            {"id": "DRSM09131", "name": "topwear3", "category": "topwear", "tags": ["party", "fancy", "elegant", "silk", "cotton","pink","off_shoulder","light","date"], "image": "DRSM09131.jpeg"},
            {"id": "DRSM09132", "name": "topwear5", "category": "topwear", "tags": ["party", "fancy", "elegant", "silk", "cotton","blue","off_shoulder","light","date"], "image": "DRSM09132.jpeg"},
            {"id": "DRSM09134", "name": "topwear6", "category": "topwear", "tags": ["party", "fancy", "elegant", "silk", "cotton","blue","off_shoulder","dark","beach","date"], "image": "DRSM09134.jpeg"},
            {"id": "DRSM09135", "name": "topwear7", "category": "topwear", "tags": ["party", "fancy", "elegant", "silk", "cotton","blue","off_shoulder","wedding","date"], "image": "DRSM09135.jpeg"},
            {"id": "DRSM09136", "name": "topwear9", "category": "topwear", "tags": ["party", "fancy", "elegant", "silk", "cotton","black","off_shoulder","wedding","date"], "image": "DRSM09136.jpeg"},
            {"id": "DRSM09137", "name": "topwear10", "category": "topwear", "tags": ["party", "fancy", "elegant", "leather", "black","outing","date"], "image": "DRSM09137.jpeg"},
            {"id": "DRSM09138", "name": "topwear11", "category": "topwear", "tags": ["party", "fancy", "elegant", "silk", "cotton","white","cream","wedding","date"], "image": "DRSM09138.jpeg"},
            {"id": "DRSM09139", "name": "topwear12", "category": "topwear", "tags": ["party", "fancy", "elegant", "silk", "cotton","gray","date"], "image": "DRSM09139.jpeg"},
            {"id": "DRSM09140", "name": "topwear13", "category": "topwear", "tags": ["party", "fancy", "elegant", "silk", "cotton","white","cream"], "image": "DRSM09140.jpeg"},
            {"id": "DRSM09141", "name": "topwear14", "category": "topwear", "tags": ["party", "fancy", "elegant", "silk", "cotton","pink"], "image": "DRSM09141.jpeg"},
            {"id": "DRSM09142", "name": "topwear15", "category": "topwear", "tags": ["party", "fancy", "elegant", "silk", "cotton","green","light","formal","date"], "image": "DRSM09142.jpeg"},
            {"id": "DRSM09143", "name": "topwear16", "category": "topwear", "tags": ["party", "fancy", "elegant", "silk", "cotton","blue","formal","date"], "image": "DRSM09143.jpeg"},
            {"id": "DRSM09144", "name": "topwear17", "category": "topwear", "tags": ["party", "fancy", "elegant", "silk", "cotton","white","cream","office"], "image": "DRSM09144.jpeg"},
            {"id": "DRSM09145", "name": "topwear18", "category": "topwear", "tags": ["party", "fancy", "elegant", "silk", "cotton","blue"], "image": "DRSM09145.jpeg"},
            {"id": "DRSM09146", "name": "topwear19", "category": "topwear", "tags": ["party", "fancy", "elegant", "silk", "cotton","green"], "image": "DRSM09146.jpeg"},
            {"id": "DRSM09147", "name": "topwear20", "category": "topwear", "tags": ["office","cotton","red","formal"], "image": "DRSM09147.jpeg"},
            {"id": "DRSM09148", "name": "layer21", "category": "layer", "tags": ["party", "fancy", "elegant", "silk", "cotton","pink","blazer"], "image": "DRSM09148.jpeg"},
            {"id": "DRSM09149", "name": "layer22", "category": "layer", "tags": ["party", "fancy", "elegant", "silk", "cotton","cream","white","blazer"], "image": "DRSM09149.jpeg"},
            {"id": "DRSM09150", "name": "layer23", "category": "layer", "tags": ["party", "fancy", "elegant", "silk", "cotton","violet","purple","lavender","blazer"], "image": "DRSM09150.jpeg"},
            {"id": "DRSM09151", "name": "layer24", "category": "layer", "tags": ["cotton","black","formal","office","blazer","warm"], "image": "DRSM09151.jpeg"},
            {"id": "DRSM09153", "name": "bottom1", "category": "bottomwear", "tags": ["party","cotton", "pink","light","fancy","elegant","date"], "image": "DRSM09153.jpeg"},
            {"id": "DRSM09154", "name": "bottom2", "category": "bottomwear", "tags": ["party","cotton", "green","light","fancy","elegant","olive","date"], "image": "DRSM09154.jpeg"},
            {"id": "DRSM09155", "name": "topwear21", "category": "topwear", "tags": ["casual", "top", "shopping", "outing", "white","cream","cotton","picnic"], "image": "DRSM09155.jpeg"},
            {"id": "DRSM09156", "name": "topwear22", "category": "topwear", "tags": ["casual", "top", "shopping", "outing", "brown","cotton","picnic"], "image": "DRSM09156.jpeg"},
            {"id": "DRSM09157", "name": "topwear23", "category": "topwear", "tags": ["casual", "top", "shopping", "outing", "white","brown","stripped","cotton","picnic"], "image": "DRSM09157.jpeg"},
            {"id": "DRSM09158", "name": "topwear24", "category": "topwear", "tags": ["casual", "top", "shopping", "outing", "red","stripped","cotton","picnic"], "image": "DRSM09158.jpeg"},
            {"id": "DRSM09159", "name": "bottom3", "category": "bottomwear", "tags": ["pink","light","picnic","party","date"], "image": "DRSM09159.jpeg"},
            {"id": "DRSM09160", "name": "one_piece11", "category": "one_piece", "tags": ["party", "silk", "black","gold","fancy","elegant","office_party","one_piece","cotton","wedding","stylish"], "image": "DRSM09160.jpeg"},
            {"id": "DRSM09161", "name": "one_piece12", "category": "one_piece", "tags": ["party", "silk", "purple","violet","fancy","elegant","wedding","one_piece","cotton","stylish"], "image": "DRSM09161.jpeg"},
            {"id": "DRSM09162", "name": "one_piece13", "category": "one_piece", "tags": ["party", "silk", "purple","violet","fancy","elegant","wedding","one_piece","beach","cotton","stylish"], "image": "DRSM09162.jpeg"},
            {"id": "DRSM09163", "name": "one_piece14", "category": "one_piece", "tags": ["party", "silk", "pink","cotton","fancy","elegant","wedding","one_piece","beach","stylish"], "image": "DRSM09163.jpeg"},
            {"id": "DRSM09164", "name": "one_piece15", "category": "one_piece", "tags": ["party", "silk", "red","cotton","fancy","elegant","wedding","one_piece"], "image": "DRSM09164.jpeg"},
            {"id": "DRSM09165", "name": "topwear_88", "category": "layer", "tags": ["formal", "office", "cotton", "purple","violet","lavender"], "image": "DRSM09165.jpeg"},
            {"id": "DRSM09166", "name": "topwear_77", "category": "topwear", "tags": ["office_party", "cotton", "grey","fancy","offshoulder","party","stylish"], "image": "DRSM09166.jpeg"},
            {"id": "DRSM09167", "name": "layer_15", "category": "layer", "tags": ["formal", "office", "blazer", "green","business_meeting","interview"], "image": "DRSM09167.jpeg"},
            {"id": "DRSM09168", "name": "bottom_766", "category": "bottomwear", "tags": ["beach_party", "leather", "short", "skirt","black"], "image": "DRSM09168.jpeg"},
            {"id": "DRSM09169", "name": "bottom_767", "category": "bottomwear", "tags": ["gym", "sporty", "breathable", "blue","hiking","running","climbing","camping","exercise","trekking","yoga","mountain_climbing"], "image": "DRSM09169.jpeg"},
            {"id": "DRSM09170", "name": "bottom_768", "category": "bottomwear", "tags": ["gym", "sporty", "breathable", "brown","hiking","running","climbing","camping","exercise","trekking","yoga","mountain_climbing"], "image": "DRSM09170.jpeg"},
            {"id": "DRSM09171", "name": "bottom_769", "category": "bottomwear", "tags": [ "white","ethnic","ritual","traditional","festival","home_ritual"], "image": "DRSM09171.jpeg"},
            {"id": "DRSM09172", "name": "bottom_770", "category": "bottomwear", "tags": ["gym", "sporty", "breathable", "black","hiking","running","climbing","camping","exercise","trekking","yoga","mountain_climbing"], "image": "DRSM09172.jpeg"},
            {"id": "DRSM09173", "name": "gym_top156", "category": "topwear", "tags": ["gym", "sporty", "breathable", "white","hiking","running","climbing","camping","exercise","trekking","yoga","mountain_climbing"], "image": "DRSM09173.jpeg"},
        
        ]

if __name__ == "__main__":
    recommender = SmartOutfitRecommender(wardrobe_db)
    print("Smart Outfit Recommender")
    print("-----------------------")
    print("Enter your outfit request (e.g. 'gym outfit in green')")
    print("Type 'exit' or 'quit' to end the program")
    while True:
        prompt = input("\nWhat would you like to wear today? ").strip()
        if prompt.lower() in ['exit', 'quit']:
            break
        # Ignore numeric or empty prompts (user just enters 1, 2, 3, etc.)
        if not prompt or prompt.isdigit():
            print("\nPlease enter a valid outfit request (not just a number).")
            continue
        result = recommender.recommend_outfits(prompt)
        # Print summary in terminal
        print(f"\nContext: Time: {result['context']['time']}, Weather: {result['context']['weather']}")
        print(f"Occasion: {result['occasion'].replace('_', ' ').title()}")
        for idx, outfit in enumerate(result["outfits"], 1):
            print(f"\nOutfit {idx}: {outfit.get('reason', 'Outfit')}")
            for item in outfit["items"]:
                print(f"  - {item['name']} ({item['category']})")
                print(f"    ID: {item['id']}")
                print(f"    Tags: {', '.join(item['tags'])}")
        # Generate and open HTML with images
        html_path = recommender.generate_outfit_html(result["outfits"], filename="outfits.html")
        print(f"\nVisualize these outfits: file://{html_path}")
        webbrowser.open(f'file://{html_path}')



#1