import datetime
from collections import defaultdict


class OutfitRecommender:
    def __init__(self):
        self.keywords = [
            # Occasions
            "casual", "formal", "party", "wedding", "beach", "gym", "interview", "festive",
            "rooftop", "office", "date_night", "home_ritual", "ceremony", "semi_formal", "hiking",
            "picnic", "camping", "shopping", "funeral", "ritual", "business_meeting", "mountain_climbing", "swimming", "temple", "date",
            # Times
            "morning", "afternoon", "evening", "night",
            # Weather
            "hot", "cold", "humid", "rainy", "winter", "summer", "monsoon", "pleasant",
            # Fabrics
            "cotton", "linen", "wool", "leather", "silk", "lightweight", "breathable", "airy",
            "sleeveless", "layered", "quick_dry", "water_resistant", "waterproof", "stretchable",
            # Styles
            "bohemian", "classy", "casual", "edgy", "chic", "trendy", "vintage", "modern", "fancy", "stylish", "elegant", "traditional", "ethnic", "western", "fusion",
            # Colors
            "red", "blue", "yellow", "peach", "black", "green", "purple", "pink", "white",
            "grey", "cream", "gold", "silver", "beige", "brown", "maroon", "teal",
            "aquamarine", "orange", "turquoise", "lavender", "mint", "navy", "coral",
            "mustard", "olive", "khaki", "charcoal", "light_blue",
            # Types
            "one_piece", "swimwear", "modest", "durable", "comfortable"
        ]
        self.color_complements = {
            "red": ["gold", "cream", "white", "black", "maroon"],
            "blue": ["white", "grey", "silver", "navy", "yellow"],
            "yellow": ["peach", "white", "mint", "grey", "blue"],
            "pink": ["white", "cream", "peach", "grey", "green"],
            "maroon": ["gold", "cream", "beige", "navy", "red"],
            "teal": ["white", "gold", "peach", "brown", "mustard"],
            "purple": ["silver", "white", "pink", "black", "lavender"],
            "navy": ["white", "beige", "gold", "pink", "red"],
            "gold": ["maroon", "navy", "black", "green", "cream", "red"],
            "cream": ["maroon", "red", "navy", "green", "gold"],
            "green": ["gold", "cream", "white", "black", "brown"],
            "orange": ["teal", "navy", "olive", "cream", "brown"]
        }
        self.user_preferences = {
            "preferred_colors": [],
            "preferred_styles": [],
            "preferred_fabrics": [],
            "avoid_colors": [],
            "avoid_styles": []
        }
        self.wardrobe_db = self.load_wardrobe_db()
        self.user_selections = defaultdict(int)

    def load_wardrobe_db(self):
         return [
            # --- Picnic & Outdoor ---
            {"id": "DRSM09001", "name": "picnic_top1", "category": "topwear", "tags": ["picnic", "casual", "comfortable", "lightweight", "cotton", "red","sleeve_less"], "image": "static/DRSM09001.jpeg"},
            {"id": "DRSM09002", "name": "picnic_top2", "category": "topwear", "tags": ["picnic", "casual", "comfortable", "cotton", "white"], "image": "static/DRSM09002.jpeg"},
            {"id": "DRSM09003", "name": "picnic_bottom1", "category": "bottomwear", "tags": ["picnic", "casual", "comfortable", "cotton", "blue","shorts"], "image": "static/DRSM09003.jpeg"},
            {"id": "DRSM09004", "name": "picnic_bottom2", "category": "bottomwear", "tags": ["picnic", "casual", "comfortable", "linen", "black"], "image": "static/DRSM09004.jpeg"},
            {"id": "DRSM09005", "name": "picnic_layer1", "category": "layer", "tags": ["picnic", "casual", "sweater", "white"], "image": "static/DRSM09005.jpeg"},


            # --- Hiking & Camping ---
            {"id": "DRSM09006", "name": "hiking_top1", "category": "topwear", "tags": ["hiking", "durable", "cotton", "green"],"image": "static/DRSM09006.jpeg"},
            {"id": "DRSM09007", "name": "hiking_top2", "category": "topwear", "tags": ["hiking", "durable", "breathable", "white","tank_top","sleeve_less"],"image": "static/DRSM09007.jpeg"},
            {"id": "DRSM09008", "name": "hiking_bottom1", "category": "bottomwear", "tags": ["hiking", "durable", "comfortable", "cream","white"], "image": "static/DRSM09008.jpeg"},
            {"id": "DRSM09009", "name": "hiking_bottom2", "category": "bottomwear", "tags": ["hiking", "durable", "comfortable", "black","grey"], "image": "static/DRSM09009.jpeg"},
            {"id": "DRSM09010", "name": "hiking_layer1", "category": "layer", "tags": ["hiking", "layered", "jacket", "black"], "image": "static/DRSM09010.jpeg"},

            {"id": "DRSM09011", "name": "camping_top1", "category": "topwear", "tags": ["camping", "durable", "cotton", "blue","aquamarine","comfortable","half-sleeve"], "image": "static/DRSM09011.jpeg"},
            {"id": "DRSM09012", "name": "camping_bottom1", "category": "bottomwear", "tags": ["camping", "comfortable", "cotton", "black"] ,"image": "static/DRSM09012.jpeg"},

            # --- Shopping & Casual Outing ---
            {"id": "DRSM09013", "name": "shopping_top1", "category": "topwear", "tags": ["shopping", "casual", "comfortable", "lightweight", "purple","violet","lavender"] ,"image": "static/DRSM09013.jpeg"},
            {"id": "DRSM09014", "name": "shopping_top2", "category": "topwear", "tags": ["shopping", "casual", "comfortable", "cotton", "brown","cream"] ,"image": "static/DRSM09014.jpeg"},
            {"id": "DRSM09015", "name": "shopping_bottom1", "category": "bottomwear", "tags": ["shopping", "casual", "comfortable", "denim", "blue","dark-blue","jeans"], "image": "static/DRSM09015.jpeg"},
            {"id": "DRSM09016", "name": "shopping_bottom2", "category": "bottomwear", "tags": ["shopping", "casual", "comfortable", "linen", "white","cotton","jeans"], "image": "static/DRSM09016.jpeg"},

            # --- Funeral & Formal Black ---
            {"id": "DRSM09017", "name": "funeral_top1", "category": "topwear", "tags": ["funeral", "formal", "modest", "cotton", "black"], "image": "static/DRSM09017.jpeg"},
            {"id": "DRSM09018", "name": "funeral_bottom1", "category": "bottomwear", "tags": ["funeral", "formal", "modest", "cotton", "black"], "image": "static/DRSM09018.jpeg"},

            # --- Rituals & Temple ---
            {"id": "DRSM09019", "name": "ritual_top1", "category": "topwear", "tags": ["ritual", "traditional", "modest", "cotton", "green","pine-green"], "image": "static/DRSM09019.jpeg"},
            {"id": "DRSM09020", "name": "ritual_bottom1", "category": "bottomwear", "tags": ["ritual", "traditional", "modest", "cotton", "cream","white"], "image": "static/DRSM09020.jpeg"},
            {"id": "DRSM09021", "name": "temple_visit_top1", "category": "topwear", "tags": ["temple", "traditional", "modest", "cotton", "pink"], "image": "static/DRSM09021.jpeg"},
            {"id": "DRSM09022", "name": "temple_visit_bottom1", "category": "bottomwear", "tags": ["temple", "traditional", "modest", "cotton", "black","navy","blue"], "image": "static/DRSM09022.jpeg"},

            # --- Business & Interview ---
            {"id": "DRSM09023", "name": "business_meeting_top1", "category": "topwear", "tags": ["business_meeting", "formal", "office", "professional", "cotton", "black"], "image": "static/DRSM09023.jpeg"},
            {"id": "DRSM09024", "name": "business_meeting_bottom1", "category": "bottomwear", "tags": ["business_meeting", "formal", "office", "professional",  "grey"], "image": "static/DRSM09024.jpeg"},
            {"id": "DRSM09025", "name": "interview_top1", "category": "topwear", "tags": ["interview", "formal", "cotton", "red"], "image": "static/DRSM09025.jpeg"},
            {"id": "DRSM09026", "name": "interview_bottom1", "category": "bottomwear", "tags": ["interview", "formal", "cotton", "white"], "image": "static/DRSM09026.jpeg"},
            {"id": "DRSM09027", "name": "interview_specific_top1", "category": "topwear", "tags": ["interview", "formal", "cotton", "white"],"image": "static/DRSM09027.jpeg"},
            {"id": "DRSM09028", "name": "interview_specific_bottom1", "category": "bottomwear", "tags": ["interview", "formal",  "black"], "image": "static/DRSM09028.jpeg"},
            {"id": "DRSM09029", "name": "interview_specific_layer1", "category": "layer", "tags": ["interview", "formal", "blazer", "black"], "image": "static/DRSM09029.jpeg"},

            # --- Office & Formal ---
            {"id": "DRSM09030", "name": "formal_office_top1", "category": "topwear", "tags": ["formal", "office", "cotton", "grey","brown"], "image": "static/DRSM09030.jpeg"},
            {"id": "DRSM09031", "name": "formal_office_top2", "category": "topwear", "tags": ["formal", "office", "linen", "orange","pink"], "image": "static/DRSM09031.jpeg"},
            {"id": "DRSM09032", "name": "formal_office_bottom1", "category": "bottomwear", "tags": ["formal", "office", "cotton", "white"], "image": "static/DRSM09032.jpeg"},
            {"id": "DRSM09033", "name": "formal_office_bottom2", "category": "bottomwear", "tags": ["formal", "office", "cotton", "black"], "image": "static/DRSM09033.jpeg"},
            {"id": "DRSM09034", "name": "formal_office_layer1", "category": "layer", "tags": ["formal", "office", "blazer", "black"], "image": "static/DRSM09034.jpeg"},
            {"id": "DRSM09035", "name": "formal_office_layer2", "category": "layer", "tags": ["formal", "office", "blazer", "white"], "image": "static/DRSM09035.jpeg"},

            # --- Semi-Formal & Fusion-Formal ---
            {"id": "DRSM09036", "name": "semi_formal_top1", "category": "topwear", "tags": ["semi_formal", "office", "cotton","apricot", "red","sleeveless"], "image": "static/DRSM09036.jpeg"},
            {"id": "DRSM09037", "name": "semi_formal_top2", "category": "topwear", "tags": ["semi_formal", "office", "cotton", "green","olive_green","sleeveless"], "image": "static/DRSM09037.jpeg"},
            {"id": "DRSM09038", "name": "semi_formal_bottom1", "category": "bottomwear", "tags": ["semi_formal", "office", "cotton", "white","party"], "image": "static/DRSM09038.jpeg"},
            {"id": "DRSM09039", "name": "semi_formal_layer1", "category": "layer", "tags": ["semi_formal", "office", "jacket", "black","blazer"], "image": "static/DRSM09039.jpeg"},
            {"id": "DRSM09040", "name": "fusion_formal_top1", "category": "topwear", "tags": ["fusion", "formal", "modern", "cotton", "white","black"], "image": "static/DRSM09040.jpeg"},
            {"id": "DRSM09041", "name": "fusion_formal_bottom1", "category": "bottomwear", "tags": ["fusion", "formal", "modern", "linen", "black"], "image": "static/DRSM09041.jpeg"},
            {"id": "DRSM09042", "name": "fusion_formal_layer1", "category": "layer", "tags": ["fusion", "formal", "modern", "jacket", "brown","blazer"], "image": "static/DRSM09042.jpeg"},

            # --- Party & Office Party ---
            {"id": "DRSM09043", "name": "party_top1", "category": "topwear", "tags": ["party", "stylish", "cotton", "green","dark_green"], "image": "static/DRSM09043.jpeg"},
            {"id": "DRSM09044", "name": "party_top2", "category": "topwear", "tags": ["party", "trendy", "fancy", "blue","silk","satin"], "image": "static/DRSM09044.jpeg"},
            {"id": "DRSM09045", "name": "party_bottom1", "category": "bottomwear", "tags": ["party", "trendy", "silk","cotton", "blue"], "image": "static/DRSM09045.jpeg"},
            {"id": "DRSM09046", "name": "party_bottom2", "category": "bottomwear", "tags": ["party", "stylish", "silk","cotton", "brown"], "image": "static/DRSM09046.jpeg"},
            {"id": "DRSM09047", "name": "party_bottom3", "category": "bottomwear", "tags": ["party", "stylish", "silk","cotton", "black"], "image": "static/DRSM09047.jpeg"},
            {"id": "DRSM09048", "name": "party_bottom4", "category": "bottomwear", "tags": ["party", "stylish", "silk","cotton", "white"], "image": "static/DRSM09048.jpeg"},
            {"id": "DRSM09049", "name": "party_layer1", "category": "layer", "tags": ["party", "blazer","wool" "black"], "image": "static/DRSM09049.jpeg"},
            {"id": "DRSM09050", "name": "party_layer2", "category": "layer", "tags": ["party", "elegant", "pink","blazer","wool"], "image": "static/DRSM09050.jpeg"},
            {"id": "DRSM09051", "name": "office_party_top1", "category": "topwear", "tags": ["party", "office", "stylish", "silk", "lavender","violet","purple","cotton"], "image": "static/DRSM09051.jpeg"},
            {"id": "DRSM09052", "name": "office_party_top2", "category": "topwear", "tags": ["party", "office", "trendy", "silk","cotton", "red"], "image": "static/DRSM09052.jpeg"},
            {"id": "DRSM09053", "name": "office_party_bottom1", "category": "bottomwear", "tags": ["party", "office", "trendy", "silk","cotton", "red"], "image": "static/DRSM09053.jpeg"},
            {"id": "DRSM09054", "name": "office_party_bottom2", "category": "bottomwear", "tags": ["party", "office", "stylish", "silk","cotton", "pink"], "image": "static/DRSM09054.jpeg"},
            {"id": "DRSM09055", "name": "office_party_layer1", "category": "layer", "tags": ["party", "office", "blazer","wool","cotton" "white"], "image": "static/DRSM09055.jpeg"},
            {"id": "DRSM09056", "name": "office_party_layer2", "category": "layer", "tags": ["party", "office", "elegant", "brown","blazer","cotton","wool"], "image": "static/DRSM09056.jpeg"},

            # --- Wedding (Formal & Stylish) ---
            {"id": "DRSM09057", "name": "wedding_one_piece1", "category": "one_piece", "tags": ["wedding", "formal", "stylish", "silk", "blue", "one_piece"], "image": "static/DRSM09057.jpeg"},
            {"id": "DRSM09058", "name": "wedding_one_piece2", "category": "one_piece", "tags": ["wedding", "elegant", "embroidered", "white", "one_piece","synthetic"], "image": "static/DRSM09058.jpeg"},
            {"id": "DRSM09059", "name": "wedding_formal_top1", "category": "topwear", "tags": ["wedding", "formal", "silk", "black","netted","breathable"], "image": "static/DRSM09059.jpeg"},
            {"id": "DRSM09060", "name": "wedding_formal_bottom1", "category": "bottomwear", "tags": ["wedding", "formal", "cotton", "black"], "image": "static/DRSM09060.jpeg"},
            {"id": "DRSM09061", "name": "wedding_formal_layer1", "category": "layer", "tags": ["wedding", "formal", "blazer", "whit"], "image": "static/DRSM09061.jpeg"},
            {"id": "DRSM09062", "name": "wedding_stylish_top1", "category": "topwear", "tags": ["wedding", "stylish", "embroidered", "white"], "image": "static/DRSM09062.jpeg"},
            {"id": "DRSM09063", "name": "wedding_stylish_bottom1", "category": "bottomwear", "tags": ["wedding", "stylish", "silk", "white","cotton"], "image": "static/DRSM09063.jpeg"},
            {"id": "DRSM09064", "name": "wedding_stylish_layer1", "category": "layer", "tags": ["wedding", "stylish", "blazer", "black"], "image": "static/DRSM09064.jpeg"},

            # --- Ethnic & Festive ---
            {"id": "DRSM09065", "name": "ethnic_festive_top1", "category": "topwear", "tags": ["festive", "ethnic", "embroidered", "blue","cotton","silk"], "image": "static/DRSM09065.jpeg"},
            {"id": "DRSM09066", "name": "ethnic_festive_bottom1", "category": "bottomwear", "tags": ["festive", "ethnic", "silk", "gold","cream","white","cotton"], "image": "static/DRSM09066.jpeg"},
            {"id": "DRSM09067", "name": "ethnic_festive_layer1", "category": "layer", "tags": ["festive", "ethnic", "long", "black"], "image": "static/DRSM09067.jpeg"},

            # --- Fusion & Modern ---
            {"id": "DRSM09068", "name": "fusion_top1", "category": "topwear", "tags": ["fusion", "modern", "cotton", "red"], "image": "static/DRSM09068.jpeg"},
            {"id": "DRSM09069", "name": "fusion_bottom1", "category": "bottomwear", "tags": ["fusion", "modern", "linen", "black","cotton"], "image": "static/DRSM09069.jpeg"},
            {"id": "DRSM09070", "name": "fusion_layer1", "category": "layer", "tags": ["fusion", "modern", "blazer", "black"], "image": "static/DRSM09070.jpeg"},

            # --- Date Night & Rooftop Party ---
            {"id": "DRSM09071", "name": "date_night_top1", "category": "topwear", "tags": ["date_night", "stylish", "silk", "black"], "image": "static/DRSM09071.jpeg"},
            {"id": "DRSM09072", "name": "date_night_bottom1", "category": "bottomwear", "tags": ["date_night", "trendy", "jeans", "blue","cotton"], "image": "static/DRSM09072.jpeg"},
            {"id": "DRSM09073", "name": "date_night_layer1", "category": "layer", "tags": ["date_night", "wool","cotton","blazer", "black"], "image": "static/DRSM09073.jpeg"},
            {"id": "DRSM09074", "name": "rooftop_party_top1", "category": "topwear", "tags": ["rooftop", "party", "stylish", "silk", "green","cotton"], "image": "static/DRSM09074.jpeg"},
            {"id": "DRSM09075", "name": "rooftop_party_bottom1", "category": "bottomwear", "tags": ["rooftop", "party", "trendy", "linen", "white","cotton"], "image": "static/DRSM09075.jpeg"},
            {"id": "DRSM09076", "name": "rooftop_party_layer1", "category": "layer", "tags": ["rooftop", "party", "cotton","blazer", "brown"], "image": "static/DRSM09076.jpeg"},

            # --- Home Ritual & Versatile Formal ---
            {"id": "DRSM09077", "name": "home_ritual_top1", "category": "topwear", "tags": ["home_ritual", "traditional", "cotton", "blue","silk"], "image": "static/DRSM09077.jpeg"},
            {"id": "DRSM09078", "name": "home_ritual_bottom1", "category": "bottomwear", "tags": ["home_ritual", "traditional", "cotton", "white","cream","silk"], "image": "static/DRSM09078.jpeg"},
            {"id": "DRSM09079", "name": "home_ritual_layer1", "category": "layer", "tags": ["home_ritual", "traditional", "embroidered", "white","long",], "image": "static/DRSM09079.jpeg"},
            {"id": "DRSM09080", "name": "versatile_formal_top1", "category": "topwear", "tags": ["silk", "party", "fancy", "cotton", "blue","sleeveless"], "image": "static/DRSM09080.jpeg"},
            {"id": "DRSM09081", "name": "versatile_formal_top2", "category": "topwear", "tags": ["cotton", "party", "fancy", "silk", "white"], "image": "static/DRSM09081.jpeg"},
            {"id": "DRSM09082", "name": "versatile_formal_bottom1", "category": "bottomwear", "tags": ["casual", "fancy", "denim", "jeans", "blue"], "image": "static/DRSM09082.jpeg"},
            {"id": "DRSM09083", "name": "versatile_formal_bottom2", "category": "bottomwear", "tags": ["casual", "fancy", "party", "cotton", "black"], "image": "static/DRSM09083.jpeg"},
            {"id": "DRSM09084", "name": "versatile_formal_layer1", "category": "layer", "tags": ["elegant", "fancy", "party", "blazer", "black"], "image": "static/DRSM09084.jpeg"},
            {"id": "DRSM09085", "name": "versatile_formal_layer2", "category": "layer", "tags": ["elegant", "fancy", "party", "blazer", "brown"], "image": "static/DRSM09085.jpeg"},

            # --- Casual, Gym, Beach, Rainy, Winter ---
            {"id": "DRSM09086", "name": "casual_top1", "category": "topwear", "tags": ["casual", "cotton", "lightweight", "white"], "image": "static/DRSM09086.jpeg"},
            {"id": "DRSM09087", "name": "casual_top2", "category": "topwear", "tags": ["casual", "cotton", "half_sleeve", "yellow"], "image": "static/DRSM09087.jpeg"},
            {"id": "DRSM09088", "name": "casual_bottom1", "category": "bottomwear", "tags": ["casual", "black", "jeans"], "image": "static/DRSM09088.jpeg"},
            {"id": "DRSM09089", "name": "casual_bottom2", "category": "bottomwear", "tags": ["casual", "cotton", "blue","denim"], "image": "static/DRSM09089.jpeg"},
            {"id": "DRSM09090", "name": "casual_layer1", "category": "layer", "tags": ["casual", "jacket", "pink","white","cream"], "image": "static/DRSM09090.jpeg"},
            {"id": "DRSM09091", "name": "gym_top1", "category": "topwear", "tags": ["gym", "sporty", "breathable", "white"], "image": "static/DRSM09091.jpeg"},
            {"id": "DRSM09092", "name": "gym_bottom1", "category": "bottomwear", "tags": ["gym", "stretchable", "comfortable", "black"], "image": "static/DRSM09092.jpeg"},
            {"id": "DRSM09093", "name": "beach_top1", "category": "topwear", "tags": ["beach", "lightweight", "airy", "yellow"], "image": "static/DRSM09093.jpeg"},
            {"id": "DRSM09094", "name": "beach_bottom1", "category": "bottomwear", "tags": ["beach", "quick_dry", "yellow"], "image": "static/DRSM09094.jpeg"},
            {"id": "DRSM09095", "name": "swimwear1", "category": "one_piece", "tags": ["swimming", "beach", "quick_dry", "blue", "one_piece"], "image": "static/DRSM09095.jpeg"},
            {"id": "DRSM09096", "name": "rainy_layer1", "category": "layer", "tags": ["rainy", "waterproof", "jacket", "black"], "image": "static/DRSM09096.jpeg"},
            {"id": "DRSM09097", "name": "rainy_bottom1", "category": "bottomwear", "tags": ["rainy", "quick_dry", "blue"], "image": "static/DRSM09097.jpeg"},
            {"id": "DRSM09098", "name": "winter_layer1", "category": "layer", "tags": ["winter", "warm", "wool", "brown"], "image": "static/DRSM09098.jpeg"},
            {"id": "DRSM09099", "name": "winter_bottom1", "category": "bottomwear", "tags": ["winter", "warm", "cotton", "brown"], "image": "static/DRSM09099.jpeg"},

            # --- Extra: Date, Mountain, Fusion, Beach Party ---
            {"id": "DRSM09100", "name": "mountain_climbing_top1", "category": "topwear", "tags": ["mountain_climbing", "durable", "cotton", "green"], "image": "static/DRSM09100.jpeg"},
            {"id": "DRSM09101", "name": "mountain_climbing_bottom1", "category": "bottomwear", "tags": ["mountain_climbing", "durable", "comfortable", "green","teal"], "image": "static/DRSM09101.jpeg"},
            {"id": "DRSM09102", "name": "date_top1", "category": "topwear", "tags": ["date", "stylish", "chic", "casual", "pink"], "image": "static/DRSM09102.jpeg"},
            {"id": "DRSM09103", "name": "date_bottom1", "category": "bottomwear", "tags": ["date", "chic", "casual", "black","jeans"], "image": "static/DRSM09103.jpeg"},
            {"id": "DRSM09104", "name": "beach_party_one_piece1", "category": "one_piece", "tags": ["beach", "party", "airy", "lightweight", "pink", "one_piece"], "image": "static/DRSM09104.jpeg"},
            {"id": "DRSM09105", "name": "beach_party_one_piece2", "category": "one_piece", "tags": ["beach", "party", "airy", "lightweight", "yellow", "one_piece"], "image": "static/DRSM09105.jpeg"},
            {"id": "DRSM09106", "name": "beach_party_top1", "category": "topwear", "tags": ["beach_party", "party", "airy", "lightweight", "pink"], "image": "static/DRSM09106.jpeg"},
            {"id": "DRSM09107", "name": "beach_party_bottom1", "category": "bottomwear", "tags": ["beach_party", "party", "airy", "lightweight", "white","cream"], "image": "static/DRSM09107.jpeg"},
        ]

    def update_user_preferences(self, selected_outfit):
        for item in selected_outfit["items"]:
            for tag in item["tags"]:
                self.user_selections[tag] += 1
        top_colors = [k for k, v in self.user_selections.items() if k in self.color_complements and v > 2][:3]
        top_styles = [k for k, v in self.user_selections.items() if k in ["formal", "casual", "party", "ethnic", "western"] and v > 1][:2]
        top_fabrics = [k for k, v in self.user_selections.items() if k in ["cotton", "silk", "wool", "linen"] and v > 1][:2]
        if top_colors:
            self.user_preferences["preferred_colors"] = top_colors
        if top_styles:
            self.user_preferences["preferred_styles"] = top_styles
        if top_fabrics:
            self.user_preferences["preferred_fabrics"] = top_fabrics

    def get_context(self):
        now = datetime.datetime.now()
        hour = now.hour
        month = now.month
        if 5 <= hour < 12:
            time_of_day = "morning"
        elif 12 <= hour < 17:
            time_of_day = "afternoon"
        elif 17 <= hour < 21:
            time_of_day = "evening"
        else:
            time_of_day = "night"
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

    def extract_keywords(self, prompt):
        prompt = prompt.lower()
        required = []
        preferred = []
        forbidden = []

        activity_mapping = {
            "picnic": ["picnic", "casual", "comfortable", "lightweight"],
            "hiking": ["hiking", "durable", "comfortable", "layered"],
            "camping": ["camping", "durable", "layered", "comfortable"],
            "shopping": ["shopping", "casual", "comfortable"],
            "funeral": ["funeral", "formal", "modest", "black"],
            "ritual": ["ritual", "traditional", "modest"],
            "business meeting": ["business_meeting", "formal", "office", "professional"],
            "interview": ["interview", "formal", "office"],
            "party": ["party", "stylish"],
            "wedding": ["wedding", "formal", "stylish"],
            "swimming": ["swimming", "beach", "one_piece", "quick_dry"],
            "beach": ["beach", "airy", "lightweight"],
            "mountain": ["mountain_climbing", "durable", "layered"],
            "date": ["date", "stylish", "chic", "casual"],
            "casual": ["casual", "comfortable"],
            "one-piece": ["one_piece"],
            "one piece": ["one_piece"],
            "temple": ["temple", "traditional", "modest"],
        }
        for phrase, tags in activity_mapping.items():
            if phrase in prompt:
                required.extend(tags)
        words = prompt.split()
        all_keywords = [w for w in words if w in self.keywords]
        must_have_occasions = [
            "picnic", "hiking", "camping", "shopping", "funeral", "ritual", "business_meeting",
            "interview", "party", "wedding", "swimming", "beach", "mountain_climbing", "date", "casual", "temple"
        ]
        for kw in all_keywords:
            # Defensive: check if "for" is in prompt and there is a word after "for"
            after_for = prompt.split("for")[1].strip().split() if "for" in prompt and len(prompt.split("for")) > 1 else []
            if kw in must_have_occasions or (after_for and kw == after_for[0]):
                required.append(kw)
            else:
                preferred.append(kw)
        if "avoid" in prompt or "no " in prompt:
            for color in self.color_complements.keys():
                if f"avoid {color}" in prompt or f"no {color}" in prompt:
                    forbidden.append(color)

        # --- SMART ADDITIONS ---
        # Treat "layer", "layers", "add layer", "add layers", "blazer", "jacket" as requests for a layer
        layer_triggers = ["layer", "layers", "add layer", "add layers", "blazer", "jacket"]
        if any(trigger in prompt for trigger in layer_triggers):
            required.append("layer")
        # If user asks for "one-piece", "one piece", "dress", "gown", "jumpsuit", force 'one_piece' as required
        if "one-piece" in prompt or "one piece" in prompt or "dress" in prompt or "gown" in prompt or "jumpsuit" in prompt:
            required.append("one_piece")

        return list(set(required)), list(set(preferred)), list(set(forbidden))

    def is_universally_appropriate(self, item):
        # Silk and cotton are always appropriate for any weather/season
        tags = item.get("tags", [])
        if "cotton" in tags or "silk" in tags:
            return True
        return False

    def score_item(self, item, required_kws, preferred_kws, context):
        tags = item.get("tags", [])
        score = 0
        score += sum(20 for rk in required_kws if rk in tags)
        score += sum(10 for pk in preferred_kws if pk in tags)
        # --- SMART FABRIC HANDLING ---
        if self.is_universally_appropriate(item):
            score += 18  # Strong bonus for being all-weather
        elif context["weather"] in tags:
            score += 15
        if context["time"] in tags:
            score += 10
        if context["needs_layer"] and "layer" in item["category"]:
            score += 15
        score += sum(8 for c in self.user_preferences["preferred_colors"] if c in tags)
        score += sum(5 for s in self.user_preferences["preferred_styles"] if s in tags)
        score += sum(3 for f in self.user_preferences["preferred_fabrics"] if f in tags)
        score -= sum(10 for c in self.user_preferences["avoid_colors"] if c in tags)
        score -= sum(8 for s in self.user_preferences["avoid_styles"] if s in tags)
        return score

    def find_matching_items(self, required_kws, preferred_kws, forbidden_kws, context):
        matched_items = []
        for item in self.wardrobe_db:
            tags = item.get("tags", [])
            if any(fk in tags for fk in forbidden_kws):
                continue
            score = self.score_item(item, required_kws, preferred_kws, context)
            if score > 0:
                item["score"] = score
                matched_items.append(item)
        return matched_items

    def assemble_outfits(self, matched_items, required_kws, context):
        outfits = []
        seen_combinations = set()
        tops = [i for i in matched_items if i["category"] == "topwear"]
        bottoms = [i for i in matched_items if i["category"] == "bottomwear"]
        layers = [i for i in matched_items if i["category"] == "layer"]
        one_pieces = [i for i in matched_items if i["category"] == "one_piece" or "one_piece" in i.get("tags", [])]

        # --- SMART ONE-PIECE HANDLING ---
        if "one_piece" in required_kws or (not tops and not bottoms and one_pieces):
            for op in sorted(one_pieces, key=lambda x: x["score"], reverse=True):
                outfit = {
                    "type": "one_piece",
                    "items": [op],
                    "score": op["score"],
                    "reason": f"Perfect one-piece match for {required_kws[0] if required_kws else 'the occasion'}",
                    "color_harmony": self.get_color_harmony([op])
                }
                # If user also wanted a layer, add best matching layer
                if "layer" in required_kws and layers:
                    best_layer = max(layers, key=lambda x: x["score"])
                    outfit["items"].append(best_layer)
                    outfit["score"] += best_layer["score"]
                    outfit["reason"] += " with requested layer"
                    outfit["color_harmony"] = self.get_color_harmony(outfit["items"])
                outfits.append(outfit)
                seen_combinations.add(op["id"])
            if outfits:
                return outfits[:3]

        # --- NORMAL OUTFIT HANDLING (with/without layer) ---
        for top in sorted(tops, key=lambda x: x["score"], reverse=True)[:8]:
            for bottom in sorted(bottoms, key=lambda x: x["score"], reverse=True)[:8]:
                combo_id = f"{top['id']}+{bottom['id']}"
                if combo_id in seen_combinations:
                    continue
                color_harmony = self.get_color_harmony([top, bottom])
                style_match = len(set(top["tags"]) & set(bottom["tags"]) & set(required_kws)) >= 1
                if "harmony" in color_harmony or style_match:
                    combo_score = top["score"] + bottom["score"]
                    outfit = {
                        "type": "combination",
                        "items": [top, bottom],
                        "score": combo_score,
                        "reason": "Color-coordinated and occasion-matched outfit",
                        "color_harmony": color_harmony
                    }
                    # --- SMART LAYER HANDLING ---
                    if "layer" in required_kws and layers:
                        best_layer = max(layers, key=lambda x: x["score"])
                        outfit["items"].append(best_layer)
                        outfit["score"] += best_layer["score"]
                        outfit["reason"] += " with requested layer"
                        outfit["color_harmony"] = self.get_color_harmony(outfit["items"])
                    elif context["needs_layer"] and layers:
                        best_layer = max(layers, key=lambda x: x["score"])
                        outfit["items"].append(best_layer)
                        outfit["score"] += best_layer["score"]
                        outfit["reason"] += " with weather-appropriate layer"
                        outfit["color_harmony"] = self.get_color_harmony(outfit["items"])
                    outfits.append(outfit)
                    seen_combinations.add(combo_id)
        return sorted(outfits, key=lambda x: x["score"], reverse=True)[:3]

    def get_color_harmony(self, items):
        color_wheel = [
            "red", "orange", "yellow", "green", "teal", "blue", "navy", "purple", "pink", "brown", "beige", "cream"
        ]
        neutrals = {"black", "white", "grey", "gray", "beige", "cream", "silver", "charcoal"}
        colors = []
        for item in items:
            item_colors = [t for t in item["tags"] if t in color_wheel or t in self.color_complements or t in neutrals]
            colors.extend(item_colors)
        colors = list(dict.fromkeys(colors))
        if len(items) == 1 and ("one_piece" in items[0].get("tags", []) or items[0].get("category") == "one_piece"):
            if colors:
                if all(c in neutrals for c in colors):
                    return f"Classic neutral one-piece: {', '.join(colors)}"
                return f"One-piece in {', '.join(colors)}"
            return "One-piece in classic neutral tone"
        if colors and all(c in neutrals for c in colors):
            if len(colors) == 1:
                return f"Neutral harmony: {colors[0]}"
            return f"Classic neutral harmony: {', '.join(colors)}"
        non_neutral_colors = [c for c in colors if c not in neutrals]
        if len(set(non_neutral_colors)) == 1 and non_neutral_colors:
            return f"Monochromatic color harmony: {non_neutral_colors[0]}"
        for i, c1 in enumerate(colors):
            for c2 in colors[i+1:]:
                if c2 in self.color_complements.get(c1, []):
                    return f"Complementary color harmony: {c1} + {c2}"
        idxs = [color_wheel.index(c) for c in colors if c in color_wheel]
        idxs.sort()
        for i in range(len(idxs)-1):
            if abs(idxs[i] - idxs[i+1]) == 1 or abs(idxs[i] - idxs[i+1]) == len(color_wheel)-1:
                c1 = color_wheel[idxs[i]]
                c2 = color_wheel[idxs[i+1]]
                return f"Analogous color harmony: {c1} + {c2}"
        if len(colors) >= 3:
            idxs = [color_wheel.index(c) for c in colors if c in color_wheel]
            idxs.sort()
            for i in range(len(idxs)):
                for j in range(i+1, len(idxs)):
                    for k in range(j+1, len(idxs)):
                        d1 = (idxs[j] - idxs[i]) % len(color_wheel
                        )
                        d2 = (idxs[k] - idxs[j]) % len(color_wheel)
                        d3 = (idxs[i] - idxs[k]) % len(color_wheel)
                        if d1 == d2 == d3:
                            c1, c2, c3 = color_wheel[idxs[i]], color_wheel[idxs[j]], color_wheel[idxs[k]]
                            return f"Triadic color harmony: {c1} + {c2} + {c3}"
        if any(c in neutrals for c in colors) and any(c not in neutrals for c in colors):
            color_part = ', '.join([c for c in colors if c not in neutrals])
            neutral_part = ', '.join([c for c in colors if c in neutrals])
            return f"Balanced neutral and color: {neutral_part} with {color_part}"
        if colors:
            return f"Color combination: {', '.join(colors)}"
        return "Color harmony: classic style"

    def recommend_outfits(self, prompt):
        required_kws, preferred_kws, forbidden_kws = self.extract_keywords(prompt)
        context = self.get_context()
        required_kws.append(context["time"])
        preferred_kws.extend([context["weather"], context["season"]])
        matched_items = self.find_matching_items(required_kws, preferred_kws, forbidden_kws, context)
        if matched_items:
            outfits = self.assemble_outfits(matched_items, required_kws, context)
            if outfits:
                # Only return images of topwear, bottomwear, layer, or one_piece as per logic
                for outfit in outfits:
                    for item in outfit["items"]:
                        item["image_url"] = item["image"]
                return {
                    "type": "outfits",
                    "items": outfits,
                    "context": context
                }
        fallback_outfits = self.get_fallback_outfits(required_kws, forbidden_kws, context)
        return {
            "type": "fallback_outfits",
            "items": fallback_outfits,
            "context": context,
            "message": "No perfect matches found. Here are some alternatives:"
        }

    def get_fallback_outfits(self, required_kws, forbidden_kws, context):
        # Simple fallback: return highest scored items from each category
        matched_items = self.find_matching_items(required_kws, [], forbidden_kws, context)
        fallback = []
        for cat in ["one_piece", "topwear", "bottomwear", "layer"]:
            items = [i for i in matched_items if i["category"] == cat]
            if items:
                fallback.append({"items": [max(items, key=lambda x: x["score"])]})
        return fallback[:3]

    def display_recommendations(self, recommendations):
        print("\n🌟 Outfit Recommendations")
        print(f"Context: Time: {recommendations['context']['time']}, Weather: {recommendations['context']['weather']}")
        if recommendations["type"] == "outfits":
            for idx, outfit in enumerate(recommendations["items"]):
                print(f"\n🧥 Outfit {idx + 1} (Score: {outfit['score']:.1f}) - {outfit.get('reason', '')}")
                for item in outfit["items"]:
                    print(f" - {item['category'].upper()}: {item['id']} (Tags: {', '.join(item['tags'])})")
                    print(f"   Image: {item['image_url']}")
                if "color_harmony" in outfit and outfit["color_harmony"]:
                    print(f"   {outfit['color_harmony']}")
        else:
            print("\nNo perfect matches found. Here are some alternatives:")
            for idx, item in enumerate(recommendations["items"][0]["items"]):
                print(f"\n🧥 Item {idx + 1}:")
                print(f" - {item['category'].upper()}: {item['id']} (Tags: {', '.join(item['tags'])})")
                print(f"   Image: {item['image']}")

    def display_recommendations_html(self, recommendations, html_file="templates/index.html"):
        html = []
        html.append("<html><head><title>Outfit Recommendations</title></head><body>")
        html.append(f"<h2>Outfit Recommendations</h2>")
        html.append(f"<p>Context: Time: {recommendations['context']['time']}, Weather: {recommendations['context']['weather']}</p>")
        if recommendations["type"] == "outfits":
            for idx, outfit in enumerate(recommendations["items"]):
                html.append(f"<h3>Outfit {idx + 1} (Score: {outfit['score']:.1f}) - {outfit.get('reason', '')}</h3>")
                html.append('<table style="display:flex;gap:20px;">')
                for item in outfit["items"]:
                    img_path = item["image_url"]
                    # Always use .jpeg for clickable images
                    if img_path.endswith('.jpg'):
                        img_path = img_path[:-4] + '.jpeg'
                    html.append(
                        f'<tr style="text-align:center">'
                        f'<td>'
                        f'<a href="{img_path}" target="_blank">'
                        f'<img src="{img_path}" alt="{item["id"]}" style="width:180px">'
                        f'</a>'
                        f'</td>'
                        f'<td>'
                        f'<span>{item["category"].upper()}: {item["id"]}</span><br>'
                        f'<span>Tags: {", ".join(item["tags"])}</span>'
                        f'</td>'
                        f'</tr>'
                    )
                html.append('</table>')
                if "color_harmony" in outfit and outfit["color_harmony"]:
                    html.append(f'<div><em>{outfit["color_harmony"]}</em></div>')
        else:
            html.append("<h3>No perfect matches found. Here are some alternatives:</h3>")
            for idx, item in enumerate(recommendations["items"][0]["items"]):
                img_path = item["image"]
                if img_path.endswith('.jpg'):
                    img_path = img_path[:-4] + '.jpeg'
                html.append(
                    f'<div style="display:inline-block;text-align:center;margin:10px;">'
                    f'<a href="{img_path}" target="_blank">'
                    f'<img src="{img_path}" alt="{item["id"]}" style="width:180px;height:auto;border:1px solid #ccc;padding:4px;margin-bottom:4px;">'
                    f'</a><br>'
                    f'<span>{item["category"].upper()}: {item["id"]}</span><br>'
                    f'<span>Tags: {", ".join(item["tags"])}</span>'
                    f'</div>'
                )
        html.append("</body></html>")
        with open(html_file, "w", encoding="utf-8") as f:
            f.write("\n".join(html))
        print(f"\n[HTML] Outfit recommendations saved to {html_file}. Open this file in your browser to view and click images.")

    def run(self):
        print("Welcome to Smart Outfit Recommender!")
        print("Tell me what you need (e.g. 'formal outfit for wedding' or 'casual summer clothes')")
        while True:
            prompt = input("\nWhat type of outfit are you looking for? (or 'exit' to quit): ")
            if prompt.lower() in ['exit', 'quit']:
                break
            recommendations = self.recommend_outfits(prompt)
            self.display_recommendations(recommendations)
            # --- HTML clickable output ---
            self.display_recommendations_html(recommendations)
            if recommendations["type"] == "outfits" and recommendations["items"]:
                selected = input("\nDid you select any of these? (Enter outfit number or 'none'): ")
                if selected.isdigit() and 0 < int(selected) <= len(recommendations["items"]):
                    self.update_user_preferences(recommendations["items"][int(selected)-1])
                    print("Preferences updated based on your selection!")
        print("\nThank you for using Smart Outfit Recommender!")

if __name__ == "__main__":
    recommender = OutfitRecommender()
    recommender.run()

