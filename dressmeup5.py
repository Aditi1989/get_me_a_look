import datetime
import os
import json
import re
import webbrowser
from collections import defaultdict
import random

class SmartOutfitRecommender:
    def __init__(self):
        # Enhanced color complements dictionary 
        self.color_complements = {
            "red": ["green", "gold", "black", "white", "navy", "cream"],
            "blue": ["orange", "white", "silver", "navy", "gold", "red"],
            "yellow": ["purple", "gray", "black", "white", "navy", "green"],
            "green": ["red", "brown", "gold", "black", "white", "pink"],
            "purple": ["yellow", "mint", "white", "black", "gold", "gray"],
            "pink": ["green", "brown", "white", "navy", "gray", "black"],
            "black": ["gold", "silver", "white", "red", "pink", "navy"],
            "white": ["black", "navy", "red", "gold", "green", "purple"],
            "gray": ["yellow", "pink", "white", "black", "purple", "red"],
            "brown": ["blue", "cream", "green", "white", "pink", "beige"],
            "beige": ["brown", "green", "blue", "white", "navy", "black"],
            "navy": ["gold", "red", "white", "pink", "beige", "orange"],
            "cream": ["brown", "green", "navy", "black", "red", "purple"],
            "gold": ["black", "navy", "red", "purple", "green", "blue"],
            "silver": ["blue", "black", "white", "red", "purple", "gray"],
            "orange": ["blue", "white", "black", "green", "navy", "brown"],
            "teal": ["coral", "white", "navy", "gold", "brown", "black"],
            "maroon": ["gold", "white", "navy", "green", "gray", "beige"],
            "peach": ["navy", "white", "mint", "gray", "green", "brown"],
            "mint": ["peach", "white", "navy", "gray", "brown", "pink"],
            "lavender": ["yellow", "white", "gray", "navy", "green", "gold"],
            "olive": ["red", "white", "navy", "black", "orange", "pink"],
            "coral": ["teal", "white", "navy", "gray", "black", "gold"],
            "mustard": ["purple", "white", "navy", "black", "green", "gray"],
            "turquoise": ["coral", "white", "navy", "gold", "black", "red"],
            "charcoal": ["gold", "white", "red", "navy", "pink", "green"],
            "violet": ["yellow", "white", "gray", "navy", "gold", "green"],
            "indigo": ["gold", "white", "red", "navy", "pink", "orange"]
        }
        
        self.user_preferences = {
            "preferred_colors": [],
            "preferred_styles": [],
            "preferred_fabrics": [],
            "avoid_colors": [],
            "avoid_styles": [],
            "preferred_categories": []
        }
        self.user_pref_file = "user_preferences.json"
        self.load_user_preferences()
        
        self.style_keywords = [
            "bohemian", "classy", "edgy", "chic", "trendy", "vintage", "modern",
            "fancy", "stylish", "elegant", "traditional", "ethnic", "western", "fusion"
        ]
        
        self.fabric_keywords = [
            "cotton", "linen", "wool", "leather", "silk", "denim",
            "synthetic", "netted", "breathable", "quick_dry"
        ]
        
        self.weather_considerations = {
            "hot": ["lightweight", "airy", "breathable", "sleeveless", "half-sleeve"],
            "cold": ["warm", "wool", "sweater", "jacket", "layer"],
            "rainy": ["waterproof", "quick_dry"],
            "humid": ["breathable", "lightweight"]
        }
        
        self.occasion_outfit_types = {
            "interview": ["formal_top+bottom+layer", "formal_top+bottom"],
            "office": ["formal_top+bottom", "formal_top+bottom+layer"],
            "business_meeting": ["formal_top+bottom", "formal_top+bottom+layer"],
            "formal_party": ["one_piece", "formal_top+bottom+layer"],
            "party": ["one_piece", "stylish_top+bottom", "stylish_top+bottom+layer"],
            "wedding": ["one_piece", "formal_top+bottom+layer"],
            "beach": ["casual_top+bottom", "swimwear"],
            "swimming": ["swimwear"],
            "funeral": ["modest_top+bottom"],
            "ritual": ["ethnic_top+bottom"],
            "hiking": ["sporty_top+bottom"],
            "camping": ["sporty_top+bottom"],
            "mountain_climbing": ["sporty_top+bottom"],
            "date": ["stylish_top+bottom", "one_piece"],
            "picnic": ["casual_top+bottom"],
            "gym": ["sporty_top+bottom"],
            "shopping": ["casual_top+bottom"],
            "formal": ["formal_top+bottom"],
            "casual": ["casual_top+bottom"],
            "office_party": ["stylish_top+bottom", "one_piece"]
        }
        
        self.usage_history = {}
        self.recent_outfit_ids = []
        self.max_recent = 10
        
        # Wardrobe database remains the same
        self.wardrobe_db =  [
            {"id": "DRSM09001", "name": "picnic_top1", "category": "topwear", "tags": ["picnic", "casual", "comfortable", "lightweight", "cotton", "red","sleeve_less"], "image": "DRSM09001.jpeg"},
            {"id": "DRSM09002", "name": "picnic_top2", "category": "topwear", "tags": ["picnic", "casual", "comfortable", "cotton", "white"], "image": "DRSM09002.jpeg"},
            {"id": "DRSM09003", "name": "picnic_bottom1", "category": "bottomwear", "tags": ["picnic", "casual", "comfortable", "cotton", "blue","shorts"], "image": "DRSM09003.jpeg"},
            {"id": "DRSM09004", "name": "picnic_bottom2", "category": "bottomwear", "tags": ["picnic", "casual", "comfortable", "linen", "black"], "image": "DRSM09004.jpeg"},
            {"id": "DRSM09005", "name": "picnic_layer1", "category": "layer", "tags": ["picnic", "casual", "sweater", "white"], "image": "DRSM09005.jpeg"},
            {"id": "DRSM09006", "name": "hiking_top1", "category": "topwear", "tags": ["hiking", "durable", "cotton", "green"], "image": "DRSM09006.jpeg"},
            {"id": "DRSM09007", "name": "hiking_top2", "category": "topwear", "tags": ["hiking", "durable", "breathable", "white","tank_top","sleeve_less"], "image": "DRSM09007.jpeg"},
            {"id": "DRSM09008", "name": "hiking_bottom1", "category": "bottomwear", "tags": ["hiking", "durable", "comfortable", "cream","white"], "image": "DRSM09008.jpeg"},
            {"id": "DRSM09009", "name": "hiking_bottom2", "category": "bottomwear", "tags": ["hiking", "durable", "comfortable", "black","grey"], "image": "DRSM09009.jpeg"},
            {"id": "DRSM09010", "name": "hiking_layer1", "category": "layer", "tags": ["hiking", "layered", "jacket", "black"], "image": "DRSM09010.jpeg"},
            {"id": "DRSM09011", "name": "camping_top1", "category": "topwear", "tags": ["camping", "durable", "cotton", "blue","aquamarine","comfortable","half-sleeve"], "image": "DRSM09011.jpeg"},
            {"id": "DRSM09012", "name": "camping_bottom1", "category": "bottomwear", "tags": ["camping", "comfortable", "cotton", "black"], "image": "DRSM09012.jpeg"},
            {"id": "DRSM09013", "name": "shopping_top1", "category": "topwear", "tags": ["shopping", "casual", "comfortable", "lightweight", "purple","violet","lavender"], "image": "DRSM09013.jpeg"},
            {"id": "DRSM09014", "name": "shopping_top2", "category": "topwear", "tags": ["shopping", "casual", "comfortable", "cotton", "brown","cream"], "image": "DRSM09014.jpeg"},
            {"id": "DRSM09015", "name": "shopping_bottom1", "category": "bottomwear", "tags": ["shopping", "casual", "comfortable", "denim", "blue","dark-blue","jeans"], "image": "DRSM09015.jpeg"},
            {"id": "DRSM09016", "name": "shopping_bottom2", "category": "bottomwear", "tags": ["shopping", "casual", "comfortable", "linen", "white","cotton","jeans"], "image": "DRSM09016.jpeg"},
            {"id": "DRSM09017", "name": "funeral_top1", "category": "topwear", "tags": ["funeral", "formal", "modest", "cotton", "black"], "image": "DRSM09017.jpeg"},
            {"id": "DRSM09018", "name": "funeral_bottom1", "category": "bottomwear", "tags": ["funeral", "formal", "modest", "cotton", "black"], "image": "DRSM09018.jpeg"},
            {"id": "DRSM09019", "name": "ritual_top1", "category": "topwear", "tags": ["ritual", "traditional", "modest", "cotton", "green","pine-green"], "image": "DRSM09019.jpeg"},
            {"id": "DRSM09020", "name": "ritual_bottom1", "category": "bottomwear", "tags": ["ritual", "traditional", "modest", "cotton", "cream","white"], "image": "DRSM09020.jpeg"},
            {"id": "DRSM09021", "name": "temple_visit_top1", "category": "topwear", "tags": ["temple", "traditional", "modest", "cotton", "pink"], "image": "DRSM09021.jpeg"},
            {"id": "DRSM09022", "name": "temple_visit_bottom1", "category": "bottomwear", "tags": ["temple", "traditional", "modest", "cotton", "black","navy","blue"], "image": "DRSM09022.jpeg"},
            {"id": "DRSM09023", "name": "business_meeting_top1", "category": "topwear", "tags": ["business_meeting", "formal", "office", "professional", "cotton", "black"], "image": "DRSM09023.jpeg"},
            {"id": "DRSM09024", "name": "business_meeting_bottom1", "category": "bottomwear", "tags": ["business_meeting", "formal", "office", "professional", "grey"], "image": "DRSM09024.jpeg"},
            {"id": "DRSM09025", "name": "interview_top1", "category": "topwear", "tags": ["interview", "formal", "cotton", "red"], "image": "DRSM09025.jpeg"},
            {"id": "DRSM09026", "name": "interview_bottom1", "category": "bottomwear", "tags": ["interview", "formal", "cotton", "white"], "image": "DRSM09026.jpeg"},
            {"id": "DRSM09027", "name": "interview_specific_top1", "category": "topwear", "tags": ["interview", "formal", "cotton", "white"], "image": "DRSM09027.jpeg"},
            {"id": "DRSM09028", "name": "interview_specific_bottom1", "category": "bottomwear", "tags": ["interview", "formal", "black"], "image": "DRSM09028.jpeg"},
            {"id": "DRSM09029", "name": "interview_specific_layer1", "category": "layer", "tags": ["interview", "formal", "blazer", "black"], "image": "DRSM09029.jpeg"},
            {"id": "DRSM09030", "name": "formal_office_top1", "category": "topwear", "tags": ["formal", "office", "cotton", "grey","brown"], "image": "DRSM09030.jpeg"},
            {"id": "DRSM09031", "name": "formal_office_top2", "category": "topwear", "tags": ["formal", "office", "linen", "orange","pink"], "image": "DRSM09031.jpeg"},
            {"id": "DRSM09032", "name": "formal_office_bottom1", "category": "bottomwear", "tags": ["formal", "office", "cotton", "white"], "image": "DRSM09032.jpeg"},
            {"id": "DRSM09033", "name": "formal_office_bottom2", "category": "bottomwear", "tags": ["formal", "office", "cotton", "black"], "image": "DRSM09033.jpeg"},
            {"id": "DRSM09034", "name": "formal_office_layer1", "category": "layer", "tags": ["formal", "office", "blazer", "black"], "image": "DRSM09034.jpeg"},
            {"id": "DRSM09035", "name": "formal_office_layer2", "category": "layer", "tags": ["formal", "office", "blazer", "white"], "image": "DRSM09035.jpeg"},
            
            {"id": "DRSM09037", "name": "semi_formal_top2", "category": "topwear", "tags": ["semi_formal", "office", "cotton", "green","olive_green","sleeveless"], "image": "DRSM09037.jpeg"},
            {"id": "DRSM09038", "name": "semi_formal_bottom1", "category": "bottomwear", "tags": ["semi_formal", "office", "cotton", "white","party"], "image": "DRSM09038.jpeg"},
            {"id": "DRSM09039", "name": "semi_formal_layer1", "category": "layer", "tags": ["semi_formal", "office", "jacket", "black","blazer"], "image": "DRSM09039.jpeg"},
            {"id": "DRSM09040", "name": "fusion_formal_top1", "category": "topwear", "tags": ["fusion", "formal", "modern", "cotton", "white","black"], "image": "DRSM09040.jpeg"},
            {"id": "DRSM09041", "name": "fusion_formal_bottom1", "category": "bottomwear", "tags": ["fusion", "formal", "modern", "linen", "black"], "image": "DRSM09041.jpeg"},
            {"id": "DRSM09042", "name": "fusion_formal_layer1", "category": "layer", "tags": ["fusion", "formal", "modern", "jacket", "brown","blazer"], "image": "DRSM09042.jpeg"},
            {"id": "DRSM09043", "name": "party_top1", "category": "topwear", "tags": ["party", "stylish", "cotton", "green","dark_green"], "image": "DRSM09043.jpeg"},
            {"id": "DRSM09044", "name": "party_top2", "category": "topwear", "tags": ["party", "trendy", "fancy", "blue","silk","satin"], "image": "DRSM09044.jpeg"},
            {"id": "DRSM09045", "name": "party_bottom1", "category": "bottomwear", "tags": ["party", "trendy", "silk","cotton", "blue"], "image": "DRSM09045.jpeg"},
            {"id": "DRSM09046", "name": "party_bottom2", "category": "bottomwear", "tags": ["party", "stylish", "silk","cotton", "brown"], "image": "DRSM09046.jpeg"},
            {"id": "DRSM09047", "name": "party_bottom3", "category": "bottomwear", "tags": ["party", "stylish", "silk","cotton", "black"], "image": "DRSM09047.jpeg"},
            {"id": "DRSM09048", "name": "party_bottom4", "category": "bottomwear", "tags": ["party", "stylish", "silk","cotton", "white"], "image": "DRSM09048.jpeg"},
            {"id": "DRSM09049", "name": "party_layer1", "category": "layer", "tags": ["party", "blazer","wool", "black"], "image": "DRSM09049.jpeg"},
            {"id": "DRSM09050", "name": "party_layer2", "category": "layer", "tags": ["party", "elegant", "pink","blazer","wool"], "image": "DRSM09050.jpeg"},
            {"id": "DRSM09051", "name": "office_party_top1", "category": "topwear", "tags": ["party", "office", "stylish", "silk", "lavender","violet","purple","cotton"], "image": "DRSM09051.jpeg"},
            {"id": "DRSM09052", "name": "office_party_top2", "category": "topwear", "tags": ["party", "office", "trendy", "silk","cotton", "red"], "image": "DRSM09052.jpeg"},
            {"id": "DRSM09053", "name": "office_party_bottom1", "category": "bottomwear", "tags": ["party", "office", "trendy", "silk","cotton", "red"], "image": "DRSM09053.jpeg"},
            {"id": "DRSM09054", "name": "office_party_bottom2", "category": "bottomwear", "tags": ["party", "office", "stylish", "silk","cotton", "pink"], "image": "DRSM09054.jpeg"},
            {"id": "DRSM09055", "name": "office_party_layer1", "category": "layer", "tags": ["party", "office", "blazer","wool","cotton", "white"], "image": "DRSM09055.jpeg"},
            {"id": "DRSM09056", "name": "office_party_layer2", "category": "layer", "tags": ["party", "office", "elegant", "brown","blazer","cotton","wool"], "image": "DRSM09056.jpeg"},
            {"id": "DRSM09057", "name": "wedding_one_piece1", "category": "one_piece", "tags": ["wedding", "formal", "stylish", "silk", "blue", "one_piece"], "image": "DRSM09057.jpeg"},
            {"id": "DRSM09058", "name": "wedding_one_piece2", "category": "one_piece", "tags": ["wedding", "elegant", "embroidered", "white", "one_piece","synthetic"], "image": "DRSM09058.jpeg"},
            {"id": "DRSM09059", "name": "wedding_formal_top1", "category": "topwear", "tags": ["wedding", "formal", "silk", "black","netted","breathable"], "image": "DRSM09059.jpeg"},
            {"id": "DRSM09060", "name": "wedding_formal_bottom1", "category": "bottomwear", "tags": ["wedding", "formal", "cotton", "black"], "image": "DRSM09060.jpeg"},
            {"id": "DRSM09061", "name": "wedding_formal_layer1", "category": "layer", "tags": ["wedding", "formal", "blazer", "whit"], "image": "DRSM09061.jpeg"},
            {"id": "DRSM09062", "name": "wedding_stylish_top1", "category": "topwear", "tags": ["wedding", "stylish", "embroidered", "white"], "image": "DRSM09062.jpeg"},
            {"id": "DRSM09063", "name": "wedding_stylish_bottom1", "category": "bottomwear", "tags": ["wedding", "stylish", "silk", "white","cotton"], "image": "DRSM09063.jpeg"},
            {"id": "DRSM09064", "name": "wedding_stylish_layer1", "category": "layer", "tags": ["wedding", "stylish", "blazer", "black"], "image": "DRSM09064.jpeg"},
            {"id": "DRSM09065", "name": "ethnic_festive_top1", "category": "topwear", "tags": ["festive", "ethnic", "embroidered", "blue","cotton","silk"], "image": "DRSM09065.jpeg"},
            {"id": "DRSM09066", "name": "ethnic_festive_bottom1", "category": "bottomwear", "tags": ["festive", "ethnic", "silk", "gold","cream","white","cotton"], "image": "DRSM09066.jpeg"},
            {"id": "DRSM09067", "name": "ethnic_festive_layer1", "category": "layer", "tags": ["festive", "ethnic", "long", "black"], "image": "DRSM09067.jpeg"},
            {"id": "DRSM09068", "name": "fusion_top1", "category": "topwear", "tags": ["fusion", "modern", "cotton", "red"], "image": "DRSM09068.jpeg"},
            {"id": "DRSM09069", "name": "fusion_bottom1", "category": "bottomwear", "tags": ["fusion", "modern", "linen", "black","cotton"], "image": "DRSM09069.jpeg"},
            {"id": "DRSM09070", "name": "fusion_layer1", "category": "layer", "tags": ["fusion", "modern", "blazer", "black"], "image": "DRSM09070.jpeg"},
            {"id": "DRSM09071", "name": "date_night_top1", "category": "topwear", "tags": ["date_night", "stylish", "silk", "black"], "image": "DRSM09071.jpeg"},
            {"id": "DRSM09072", "name": "date_night_bottom1", "category": "bottomwear", "tags": ["date_night", "trendy", "jeans", "blue","cotton"], "image": "DRSM09072.jpeg"},
            {"id": "DRSM09073", "name": "date_night_layer1", "category": "layer", "tags": ["date_night", "wool","cotton","blazer", "black"], "image": "DRSM09073.jpeg"},
            {"id": "DRSM09074", "name": "rooftop_party_top1", "category": "topwear", "tags": ["rooftop", "party", "stylish", "silk", "green","cotton"], "image": "DRSM09074.jpeg"},
            {"id": "DRSM09075", "name": "rooftop_party_bottom1", "category": "bottomwear", "tags": ["rooftop", "party", "trendy", "linen", "white","cotton"], "image": "DRSM09075.jpeg"},
            {"id": "DRSM09076", "name": "rooftop_party_layer1", "category": "layer", "tags": ["rooftop", "party", "cotton","blazer", "brown"], "image": "DRSM09076.jpeg"},
            {"id": "DRSM09077", "name": "home_ritual_top1", "category": "topwear", "tags": ["home_ritual", "traditional", "cotton", "blue","silk"], "image": "DRSM09077.jpeg"},
            {"id": "DRSM09078", "name": "home_ritual_bottom1", "category": "bottomwear", "tags": ["home_ritual", "traditional", "cotton", "white","cream","silk"], "image": "DRSM09078.jpeg"},
            {"id": "DRSM09079", "name": "home_ritual_layer1", "category": "layer", "tags": ["home_ritual", "traditional", "embroidered", "white","long"], "image": "DRSM09079.jpeg"},
            {"id": "DRSM09080", "name": "versatile_formal_top1", "category": "topwear", "tags": ["silk", "party", "fancy", "cotton", "blue","sleeveless"], "image": "DRSM09080.jpeg"},
            {"id": "DRSM09081", "name": "versatile_formal_top2", "category": "topwear", "tags": ["cotton", "party", "fancy", "silk", "white"], "image": "DRSM09081.jpeg"},
            {"id": "DRSM09082", "name": "versatile_formal_bottom1", "category": "bottomwear", "tags": ["casual", "fancy", "denim", "jeans", "blue"], "image": "DRSM09082.jpeg"},
            {"id": "DRSM09083", "name": "versatile_formal_bottom2", "category": "bottomwear", "tags": ["casual", "fancy", "party", "cotton", "black"], "image": "DRSM09083.jpeg"},
            {"id": "DRSM09084", "name": "versatile_formal_layer1", "category": "layer", "tags": ["elegant", "fancy", "party", "blazer", "black"], "image": "DRSM09084.jpeg"},
            {"id": "DRSM09085", "name": "versatile_formal_layer2", "category": "layer", "tags": ["elegant", "fancy", "party", "blazer", "brown"], "image": "DRSM09085.jpeg"},
            {"id": "DRSM09086", "name": "casual_top1", "category": "topwear", "tags": ["casual", "cotton", "lightweight", "white"], "image": "DRSM09086.jpeg"},
            {"id": "DRSM09087", "name": "casual_top2", "category": "topwear", "tags": ["casual", "cotton", "half_sleeve", "yellow"], "image": "DRSM09087.jpeg"},
            {"id": "DRSM09088", "name": "casual_bottom1", "category": "bottomwear", "tags": ["casual", "black", "jeans"], "image": "DRSM09088.jpeg"},
            {"id": "DRSM09089", "name": "casual_bottom2", "category": "bottomwear", "tags": ["casual", "cotton", "blue","denim"], "image": "DRSM09089.jpeg"},
            {"id": "DRSM09090", "name": "casual_layer1", "category": "layer", "tags": ["casual", "jacket", "pink","white","cream"], "image": "DRSM09090.jpeg"},
            {"id": "DRSM09091", "name": "gym_top1", "category": "topwear", "tags": ["gym", "sporty", "breathable", "white"], "image": "DRSM09091.jpeg"},
            {"id": "DRSM09092", "name": "gym_bottom1", "category": "bottomwear", "tags": ["gym", "stretchable", "comfortable", "black"], "image": "DRSM09092.jpeg"},
            {"id": "DRSM09093", "name": "beach_top1", "category": "topwear", "tags": ["beach", "lightweight", "airy", "yellow"], "image": "DRSM09093.jpeg"},
            {"id": "DRSM09094", "name": "beach_bottom1", "category": "bottomwear", "tags": ["beach", "quick_dry", "yellow"], "image": "DRSM09094.jpeg"},
            {"id": "DRSM09095", "name": "swimwear1", "category": "one_piece", "tags": ["swimming", "quick_dry", "blue", "one_piece"], "image": "DRSM09095.jpeg"},
            {"id": "DRSM09096", "name": "rainy_layer1", "category": "layer", "tags": ["rainy", "waterproof", "jacket", "black"], "image": "DRSM09096.jpeg"},
            {"id": "DRSM09097", "name": "rainy_bottom1", "category": "bottomwear", "tags": ["rainy", "quick_dry", "blue"], "image": "DRSM09097.jpeg"},
            {"id": "DRSM09098", "name": "winter_layer1", "category": "layer", "tags": ["winter", "warm", "wool", "brown"], "image": "DRSM09098.jpeg"},
            {"id": "DRSM09099", "name": "winter_bottom1", "category": "bottomwear", "tags": ["winter", "warm", "cotton", "brown"], "image": "DRSM09099.jpeg"},
            {"id": "DRSM09100", "name": "mountain_climbing_top1", "category": "topwear", "tags": ["mountain_climbing", "durable", "cotton", "green"], "image": "DRSM09100.jpeg"},
            {"id": "DRSM09101", "name": "mountain_climbing_bottom1", "category": "bottomwear", "tags": ["mountain_climbing", "durable", "comfortable", "green","teal"], "image": "DRSM09101.jpeg"},
            {"id": "DRSM09102", "name": "date_top1", "category": "topwear", "tags": ["date", "stylish", "chic", "casual", "pink"], "image": "DRSM09102.jpeg"},
            {"id": "DRSM09103", "name": "date_bottom1", "category": "bottomwear", "tags": ["date", "chic", "casual", "black","jeans"], "image": "DRSM09103.jpeg"},
            {"id": "DRSM09104", "name": "beach_party_one_piece1", "category": "one_piece", "tags": ["beach", "party", "airy", "lightweight", "pink", "one_piece"], "image": "DRSM09104.jpeg"},
            {"id": "DRSM09105", "name": "beach_party_one_piece2", "category": "one_piece", "tags": ["beach", "party", "airy", "lightweight", "yellow", "one_piece"], "image": "DRSM09105.jpeg"},
            {"id": "DRSM09106", "name": "beach_party_top1", "category": "topwear", "tags": ["beach_party", "party", "airy", "lightweight", "pink"], "image": "DRSM09106.jpeg"},
            {"id": "DRSM09107", "name": "beach_party_bottom1", "category": "bottomwear", "tags": ["beach_party", "party", "airy", "lightweight", "white","cream"], "image": "DRSM09107.jpeg"},
            {"id": "DRSM09108", "name": "kurti1", "category": "topwear", "tags": ["ritual", "ethnic", "elegant", "pink", "silk", "cotton","temple","festive"], "image": "DRSM09108.jpeg"},
            {"id": "DRSM09109", "name": "kurti2", "category": "topwear", "tags": ["ritual", "ethnic", "elegant", "green", "silk", "cotton","temple","festive"], "image": "DRSM09109.jpeg"},
            {"id": "DRSM09110", "name": "kurti3", "category": "topwear", "tags": ["ritual", "ethnic", "elegant", "grey", "silk", "cotton","temple","festive"], "image": "DRSM09110.jpeg"},
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
            {"id": "DRSM09124", "name": "pants1", "category": "bottomwear", "tags": ["hiking", "durable", "cotton", "grey","black","climbing","mountain","mountain_climbing","camping","comfortable"], "image": "DRSM09124.jpeg"},
            {"id": "DRSM09125", "name": "pants2", "category": "bottomwear", "tags": ["hiking", "durable", "cotton", "green","olive","climbing","mountain","mountain_climbing","camping","comfortable"], "image": "DRSM09125.jpeg"},
            {"id": "DRSM09126", "name": "casual6", "category": "topwear", "tags": ["casual", "top", "shopping", "outing", "blue","comfortable","cotton","market"], "image": "DRSM09126.jpeg"},
            {"id": "DRSM09127", "name": "casual7", "category": "topwear", "tags": ["casual", "top", "shopping", "outing", "pink","comfortable","cotton","market"], "image": "DRSM09127.jpeg"},
            {"id": "DRSM09128", "name": "topwear1", "category": "topwear", "tags": ["party", "fancy", "elegant", "silk", "cotton","green","olive","date"], "image": "DRSM09128.jpeg"},
            {"id": "DRSM09129", "name": "topwear26", "category": "topwear", "tags": ["party", "fancy", "elegant", "silk", "cotton","green","light","date"], "image": "DRSM09129.jpeg"},
            {"id": "DRSM09130", "name": "topwear2", "category": "topwear", "tags": ["party", "fancy", "elegant", "silk", "cotton","pink","light","date"], "image": "DRSM09130.jpeg"},
            {"id": "DRSM09131", "name": "topwear3", "category": "topwear", "tags": ["party", "fancy", "elegant", "silk", "cotton","pink","off_shoulder","light","date"], "image": "DRSM09131.jpeg"},
            {"id": "DRSM09132", "name": "topwear5", "category": "topwear", "tags": ["party", "fancy", "elegant", "silk", "cotton","blue","off_shoulder","light","date"], "image": "DRSM09132.jpeg"},
            {"id": "DRSM09134", "name": "topwear6", "category": "topwear", "tags": ["party", "fancy", "elegant", "silk", "cotton","blue","off_shoulder","dark","beach","date"], "image": "DRSM09134.jpeg"},
            {"id": "DRSM09135", "name": "topwear7", "category": "topwear", "tags": ["party", "fancy", "elegant", "silk", "cotton","blue","off_shoulder","formal","wedding","date"], "image": "DRSM09135.jpeg"},
            {"id": "DRSM09136", "name": "topwear9", "category": "topwear", "tags": ["party", "fancy", "elegant", "silk", "cotton","black","off_shoulder","formal","wedding","date"], "image": "DRSM09136.jpeg"},
            {"id": "DRSM09137", "name": "topwear10", "category": "topwear", "tags": ["party", "fancy", "elegant", "leather", "black","shopping","outing","date"], "image": "DRSM09137.jpeg"},
            {"id": "DRSM09138", "name": "topwear11", "category": "topwear", "tags": ["party", "fancy", "elegant", "silk", "cotton","white","cream","wedding","date"], "image": "DRSM09138.jpeg"},
            {"id": "DRSM09139", "name": "topwear12", "category": "topwear", "tags": ["party", "fancy", "elegant", "silk", "cotton","gray","date"], "image": "DRSM09139.jpeg"},
            {"id": "DRSM09140", "name": "topwear13", "category": "topwear", "tags": ["party", "fancy", "elegant", "silk", "cotton","white","cream"], "image": "DRSM09140.jpeg"},
            {"id": "DRSM09141", "name": "topwear14", "category": "topwear", "tags": ["party", "fancy", "elegant", "silk", "cotton","pink","formal"], "image": "DRSM09141.jpeg"},
            {"id": "DRSM09142", "name": "topwear15", "category": "topwear", "tags": ["party", "fancy", "elegant", "silk", "cotton","green","light","formal","date"], "image": "DRSM09142.jpeg"},
            {"id": "DRSM09143", "name": "topwear16", "category": "topwear", "tags": ["party", "fancy", "elegant", "silk", "cotton","blue","formal","date"], "image": "DRSM09143.jpeg"},
            {"id": "DRSM09144", "name": "topwear17", "category": "topwear", "tags": ["party", "fancy", "elegant", "silk", "cotton","white","cream","office"], "image": "DRSM09144.jpeg"},
            {"id": "DRSM09145", "name": "topwear18", "category": "topwear", "tags": ["party", "fancy", "elegant", "silk", "cotton","blue","formal"], "image": "DRSM09145.jpeg"},
            {"id": "DRSM09146", "name": "topwear19", "category": "topwear", "tags": ["party", "fancy", "elegant", "silk", "cotton","green","formal"], "image": "DRSM09146.jpeg"},
            {"id": "DRSM09147", "name": "topwear20", "category": "topwear", "tags": ["office", "fancy", "elegant", "silk", "cotton","red","casual"], "image": "DRSM09147.jpeg"},
            {"id": "DRSM09148", "name": "layer21", "category": "topwear", "tags": ["party", "fancy", "elegant", "silk", "cotton","pink","office","formal","blazer"], "image": "DRSM09148.jpeg"},
            {"id": "DRSM09149", "name": "layer22", "category": "topwear", "tags": ["party", "fancy", "elegant", "silk", "cotton","cream","white","formal","office","blazer"], "image": "DRSM09149.jpeg"},
            {"id": "DRSM09150", "name": "layer23", "category": "topwear", "tags": ["party", "fancy", "elegant", "silk", "cotton","violet","purple","lavender","formal","office","blazer"], "image": "DRSM09150.jpeg"},
            {"id": "DRSM09151", "name": "layer24", "category": "topwear", "tags": ["party", "fancy", "elegant", "silk", "cotton","black","formal","office","blazer"], "image": "DRSM09151.jpeg"},
            {"id": "DRSM09152", "name": "layer25", "category": "topwear", "tags": ["party", "fancy", "elegant", "silk", "cotton","pink","light","formal","office","blazer"], "image": "DRSM09152.jpeg"},
            {"id": "DRSM09153", "name": "bottom1", "category": "bottomwear", "tags": ["party", "formal", "modest", "cotton", "pink","light","fancy","elegant"], "image": "DRSM09153.jpeg"},
            {"id": "DRSM09154", "name": "bottom2", "category": "bottomwear", "tags": ["party", "formal", "modest", "cotton", "green","light","fancy","elegant","olive"], "image": "DRSM09154.jpeg"},
            {"id": "DRSM09155", "name": "topwear21", "category": "topwear", "tags": ["casual", "top", "shopping", "outing", "white","cream","cotton","picnic","hiking","camping","mountain_climbing","climbing"], "image": "DRSM09155.jpeg"},
            {"id": "DRSM09156", "name": "topwear22", "category": "topwear", "tags": ["casual", "top", "shopping", "outing", "brown","cotton","picnic","hiking","camping","mountain_climbing","climbing"], "image": "DRSM09156.jpeg"},
            {"id": "DRSM09157", "name": "topwear23", "category": "topwear", "tags": ["casual", "top", "shopping", "outing", "white","brown","stripped","cotton","picnic","hiking","camping","mountain_climbing","climbing"], "image": "DRSM09157.jpeg"},
            {"id": "DRSM09158", "name": "topwear24", "category": "topwear", "tags": ["casual", "top", "shopping", "outing", "red","stripped","cotton","picnic"], "image": "DRSM09158.jpeg"},
            {"id": "DRSM09159", "name": "bottom3", "category": "bottomwear", "tags": ["business_meeting", "formal", "office", "professional","pink","light","picnic","party","festive"], "image": "DRSM09159.jpeg"},
            {"id": "DRSM09160", "name": "one_piece11", "category": "one_piece", "tags": ["party", "formal", "silk", "black","gold","fancy","elegant","wedding","one_piece","cotton"], "image": "DRSM09160.jpeg"},
            {"id": "DRSM09161", "name": "one_piece12", "category": "one_piece", "tags": ["party", "formal", "silk", "purple","violet","fancy","elegant","wedding","one_piece","cotton"], "image": "DRSM09161.jpeg"},
            {"id": "DRSM09162", "name": "one_piece13", "category": "one_piece", "tags": ["party", "silk", "purple","violet","fancy","elegant","wedding","one_piece","beach","cotton"], "image": "DRSM09162.jpeg"},
            {"id": "DRSM09163", "name": "one_piece14", "category": "one_piece", "tags": ["party", "silk", "pink","cotton","fancy","elegant","wedding","one_piece","beach"], "image": "DRSM09163.jpeg"},
            {"id": "DRSM09164", "name": "one_piece15", "category": "one_piece", "tags": ["party", "formal", "silk", "red","cotton","fancy","elegant","wedding","one_piece"], "image": "DRSM09164.jpeg"},
            {"id": "DRSM09165", "name": "topwear_88", "category": "layer", "tags": ["formal", "office", "cotton", "purple","violet","lavender","party"], "image": "DRSM09165.jpeg"},
            {"id": "DRSM09166", "name": "topwear_77", "category": "topwear", "tags": ["formal", "office", "cotton", "grey","fancy","offshoulder"], "image": "DRSM09166.jpeg"},
            {"id": "DRSM09167", "name": "layer_15", "category": "layer", "tags": ["formal", "office", "blazer", "green"], "image": "DRSM09167.jpeg"},
            {"id": "DRSM09168", "name": "bottom_766", "category": "bottomwear", "tags": ["beach", "leather", "short", "skirt","party","black"], "image": "DRSM09168.jpeg"},
            {"id": "DRSM09169", "name": "bottom_767", "category": "bottomwear", "tags": ["gym", "sporty", "breathable", "blue","hiking","running","climbing","camping","exercise","trekking"], "image": "DRSM09169.jpeg"},
            {"id": "DRSM09170", "name": "bottom_768", "category": "bottomwear", "tags": ["gym", "sporty", "breathable", "brown","hiking","running","climbing","camping","exercise","trekking"], "image": "DRSM09170.jpeg"},
            {"id": "DRSM09171", "name": "bottom_769", "category": "bottomwear", "tags": ["gym", "sporty", "breathable", "white","hiking","running","climbing","camping","exercise","trekking","ethnic","ritual"], "image": "DRSM09171.jpeg"},
            {"id": "DRSM09172", "name": "bottom_770", "category": "bottomwear", "tags": ["gym", "sporty", "breathable", "black","hiking","running","climbing","camping","exercise","trekking"], "image": "DRSM09172.jpeg"},
            {"id": "DRSM09173", "name": "gym_top156", "category": "topwear", "tags": ["gym", "sporty", "breathable", "white","hiking","running","climbing","camping","exercise","trekking"], "image": "DRSM09173.jpeg"},
        ]
        
        self.recent_items_per_context = defaultdict(list)
        self.max_recent_per_context = 5
        self.shown_combos_per_context = defaultdict(set)
        self.all_possible_combos = self.precompute_all_possible_combos()

    def precompute_all_possible_combos(self):
        """Precompute all possible valid combinations for each occasion type"""
        combos = defaultdict(list)
        tops = [item for item in self.wardrobe_db if item["category"] == "topwear"]
        bottoms = [item for item in self.wardrobe_db if item["category"] == "bottomwear"]
        one_pieces = [item for item in self.wardrobe_db if item["category"] == "one_piece"]
        
        for occasion in self.occasion_outfit_types:
            for top in tops:
                if occasion in top.get("tags", []):
                    for bottom in bottoms:
                        if occasion in bottom.get("tags", []):
                            combos[occasion].append((top["id"], bottom["id"]))
            
            if "one_piece" in self.occasion_outfit_types[occasion]:
                for op in one_pieces:
                    if occasion in op.get("tags", []):
                        combos[occasion].append((op["id"],))
        
        return combos

    def get_color_harmony(self, items):
        """Analyze color compatibility using complementary colors and fashion color theory"""
        color_tags = []
        for item in items:
            # Extract first valid color tag from item
            item_colors = [tag for tag in item.get("tags", []) 
                          if tag in self.color_complements]
            if item_colors:
                color_tags.append(item_colors[0])
        
        # Simple complementary check
        if len(color_tags) >= 2:
            base_color = color_tags[0]
            if any(c in self.color_complements.get(base_color, []) for c in color_tags[1:]):
                return "complementary"
        
        # Monochromatic check
        if len(set(color_tags)) == 1 and color_tags:
            return "monochromatic"
        
        # Neutral combination check
        neutrals = {"black", "white", "gray", "beige", "cream", "navy"}
        if color_tags and all(c in neutrals for c in color_tags):
            return "neutral"
        
        # Analogous check (colors adjacent on color wheel)
        color_order = list(self.color_complements.keys())
        try:
            indices = [color_order.index(c) for c in color_tags if c in color_order]
            if indices:
                max_diff = max(indices) - min(indices)
                if max_diff <= 2:  # Adjacent in the list (approximate color wheel)
                    return "analogous"
        except ValueError:
            pass
        
        return "stylish combination"

    def load_user_preferences(self):
        if os.path.exists(self.user_pref_file):
            try:
                with open(self.user_pref_file, "r") as f:
                    prefs = json.load(f)
                    self.user_preferences.update(prefs)
            except Exception:
                pass

    def save_user_preferences(self):
        with open(self.user_pref_file, "w") as f:
            json.dump(self.user_preferences, f)

    def update_user_preferences(self, chosen_outfit):
        for item in chosen_outfit["items"]:
            tags = item.get("tags", [])
            for color in self.color_complements:
                if color in tags and color not in self.user_preferences["preferred_colors"]:
                    self.user_preferences["preferred_colors"].append(color)
            for style in self.style_keywords:
                if style in tags and style not in self.user_preferences["preferred_styles"]:
                    self.user_preferences["preferred_styles"].append(style)
            for fabric in self.fabric_keywords:
                if fabric in tags and fabric not in self.user_preferences["preferred_fabrics"]:
                    self.user_preferences["preferred_fabrics"].append(fabric)
            category = item.get("category")
            if category and category not in self.user_preferences["preferred_categories"]:
                self.user_preferences["preferred_categories"].append(category)
        self.save_user_preferences()

    def get_context(self):
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

    def analyze_occasion(self, prompt):
        prompt = prompt.lower()
        occasion_mapping = {
            "office_party": ["office party", "office celebration", "work party", "corporate party"],
            "interview": ["interview"],
            "business_meeting": ["business meeting", "business", "meeting", "presentation"],
            "office": ["office", "work"],
            "formal_party": ["formal party", "gala", "cocktail"],
            "party": ["party", "celebration", "birthday", "anniversary"],
            "wedding": ["wedding", "marriage"],
            "beach": ["beach"],
            "swimming": ["swimming", "swim", "pool"],
            "funeral": ["funeral", "memorial"],
            "ritual": ["ritual", "temple", "prayer", "worship", "ceremony"],
            "hiking": ["hiking", "trekking"],
            "camping": ["camping"],
            "mountain_climbing": ["mountain climbing", "rock climbing"],
            "date": ["date", "romantic"],
            "picnic": ["picnic", "outing"],
            "gym": ["gym", "workout"],
            "shopping": ["shopping", "mall"],
            "formal": ["formal", "official"],
            "casual": ["casual", "relaxed"],
        }
        for occasion, keywords in occasion_mapping.items():
            if any(kw in prompt for kw in keywords):
                return occasion
        return "general"

    def extract_keywords(self, prompt):
        prompt = prompt.lower()
        required, preferred, forbidden = [], [], []
        
        # Extract colors
        color_matches = re.findall(r'(?:in|wearing|color|colour|shade of|like)\s+(\w+)', prompt)
        required.extend([c for c in color_matches if c in self.color_complements])
        
        # Extract avoid keywords
        avoid_matches = re.findall(r'(?:avoid|not|no|dont want|don\'t want|skip)\s+(\w+)', prompt)
        forbidden.extend([c for c in avoid_matches if c in self.color_complements])
        
        # Handle special outfit types
        if "one piece" in prompt or "dress" in prompt or "gown" in prompt:
            required.append("one_piece")
        if "swim" in prompt or "swimming" in prompt:
            required.append("swimwear")
        if "no layer" in prompt or "no jacket" in prompt or "no blazer" in prompt:
            forbidden.append("layer")
        elif "layer" in prompt or "jacket" in prompt or "blazer" in prompt:
            required.append("layer")
            
        # Extract style and fabric keywords
        for kw in self.style_keywords + self.fabric_keywords + list(self.color_complements.keys()):
            if kw in prompt:
                if "no " + kw in prompt or "not " + kw in prompt or "skip " + kw in prompt:
                    forbidden.append(kw)
                else:
                    preferred.append(kw)
                    
        return list(set(required)), list(set(preferred)), list(set(forbidden))

    def score_item(self, item, required_kws, preferred_kws, forbidden_kws, context, occasion):
        tags = set(item.get("tags", []))
        score = 0
        
        # Required keywords have highest priority
        score += sum(30 for rk in required_kws if rk in tags)
        
        # Penalize forbidden keywords heavily
        score -= sum(100 for fk in forbidden_kws if fk in tags)
        
        # Preferred keywords add moderate value
        score += sum(15 for pk in preferred_kws if pk in tags)
        
        # Contextual scoring
        if context["weather"] in tags:
            score += 20
        if context["time"] in tags:
            score += 15
            
        # Occasion scoring
        if occasion in tags:
            score += 50
        elif any(tag in tags for tag in ["formal", "casual", "party"]):
            score += 20
            
        # Weather considerations
        weather_tags = self.weather_considerations.get(context["weather"], [])
        score += sum(10 for wt in weather_tags if wt in tags)
        
        # User preferences
        score += sum(10 for c in self.user_preferences["preferred_colors"] if c in tags)
        score += sum(8 for s in self.user_preferences["preferred_styles"] if s in tags)
        score += sum(5 for f in self.user_preferences["preferred_fabrics"] if f in tags)
        score += sum(15 for cat in self.user_preferences["preferred_categories"] if item["category"] == cat)
        
        # Special cases
        if "swimwear" in required_kws and "swimwear" not in tags and "swimming" not in tags:
            score -= 1000
        if "one_piece" in required_kws and item["category"] != "one_piece":
            score -= 500
        if context["needs_layer"] and item["category"] == "layer":
            score += 30
            
        # Enhanced office/formal scoring
        if occasion in ["office", "business_meeting", "interview", "formal"]:
            if occasion in tags:
                score += 50
            if "formal" in tags:
                score += 30  # Boost truly formal items
            if "professional" in tags:
                score += 25  # Prioritize professional clothing
            # For hot weather, prioritize appropriate attire
            if context["weather"] == "hot":
                if "breathable" in tags or "lightweight" in tags:
                    score += 15
                if item["category"] == "layer" and not any(kw in required_kws for kw in ["layer", "jacket", "blazer"]):
                    score -= 40  # Heavily penalize layers in hot weather unless requested

        return score

    def find_matching_items(self, required_kws, preferred_kws, forbidden_kws, context, occasion):
        items = self.wardrobe_db

        # Special handling for party occasions
        if occasion in ["party", "wedding", "office_party", "formal_party"]:
            # Define fancy tags and tags to avoid for party wear
            fancy_tags = ["fancy", "stylish", "elegant", "party", "one_piece", "embroidered", "wedding"]
            avoid_tags = [
                "office", "business_meeting", "interview", "professional", "hiking", "sporty", "gym",
                "casual", "picnic", "shopping", "funeral", "ritual", "camping", "mountain_climbing", 
                "swimming", "swimwear", "quick_dry", "exercise", "running", "climbing", "rainy"
            ]
            
            # Get all valid one-piece items for party
            one_pieces = [
                item for item in items
                if item["category"] == "one_piece" 
                and any(tag in item["tags"] for tag in fancy_tags)
                and not any(tag in item["tags"] for tag in avoid_tags)
            ]
            
            # Filter by color if specified
            color_keywords = [kw for kw in required_kws if kw in self.color_complements]
            if color_keywords:
                color_filtered = [
                    item for item in one_pieces
                    if any(color in item["tags"] for color in color_keywords)
                ]
                if color_filtered:
                    one_pieces = color_filtered
            
            # Score one-pieces
            scored_one_pieces = []
            for item in one_pieces:
                score = self.score_item(item, required_kws, preferred_kws, forbidden_kws, context, occasion)
                if score > 0:
                    item_copy = dict(item)
                    item_copy["score"] = score * (1.5 if "one_piece" in required_kws else 1.0)
                    scored_one_pieces.append(item_copy)
            
            # If user specifically requested one-piece, prioritize them
            if "one_piece" in required_kws:
                if len(scored_one_pieces) >= 2:
                    return scored_one_pieces[:2]  # Return top 2 one-pieces
                
                # If not enough one-pieces, add fancy tops/bottoms as backup
                fancy_items = [
                    item for item in items
                    if item["category"] in ["topwear", "bottomwear"]
                    and any(tag in item["tags"] for tag in fancy_tags)
                    and not any(tag in item["tags"] for tag in avoid_tags)
                ]
                scored_fancy_items = []
                for item in fancy_items:
                    score = self.score_item(item, required_kws, preferred_kws, forbidden_kws, context, occasion)
                    if score > 0:
                        item_copy = dict(item)
                        item_copy["score"] = score * 0.7  # Slightly lower priority than one-pieces
                        scored_fancy_items.append(item_copy)
                
                # Return one-pieces first, then fancy items
                return scored_one_pieces + scored_fancy_items
            else:
                # For general party request, ensure at least one one-piece is included
                fancy_items = [
                    item for item in items
                    if item["category"] in ["topwear", "bottomwear"]
                    and any(tag in item["tags"] for tag in fancy_tags)
                    and not any(tag in item["tags"] for tag in avoid_tags)
                ]
                scored_fancy_items = []
                for item in fancy_items:
                    score = self.score_item(item, required_kws, preferred_kws, forbidden_kws, context, occasion)
                    if score > 0:
                        item_copy = dict(item)
                        item_copy["score"] = score
                        scored_fancy_items.append(item_copy)
                
                # Always include at least one one-piece at the front if available
                if scored_one_pieces:
                    return [scored_one_pieces[0]] + scored_fancy_items
                else:
                    return scored_fancy_items

        if occasion in ["party", "wedding", "beach_party", "date"]:
            # Define category lists before use
            tops = [item for item in items if item["category"] == "topwear"]
            bottoms = [item for item in items if item["category"] == "bottomwear"]
            layers = [item for item in items if item["category"] == "layer"]
            one_pieces = [item for item in items if item["category"] == "one_piece"]

            # 1. Always include one one-piece (two if specifically requested)
            outfits = []
            shown_combos = set()
            one_pieces_sorted = sorted(
                [op for op in one_pieces if any(t in op["tags"] for t in ["fancy", "elegant", "stylish"])],
                key=lambda x: x["score"],
                reverse=True
            )
            num_one_pieces = 2 if "one_piece" in required_kws else 1
            one_piece_added = 0
            for op in one_pieces_sorted:
                combo_id = (op["id"],)
                if combo_id not in shown_combos:
                    outfits.append({
                        "type": "one_piece",
                        "items": [op],
                        "score": op["score"] * 1.2,
                        "reason": f"Elegant {occasion.replace('_', ' ')} one-piece",
                        "color_harmony": self.get_color_harmony([op])
                    })
                    shown_combos.add(combo_id)
                    one_piece_added += 1
                    if one_piece_added >= num_one_pieces:
                        break

            # 2. Add top+bottom combos with maximum variety, no repetition of tops/bottoms
            if len(outfits) < 3:
                fancy_tops = sorted(
                    [t for t in tops if any(tag in t["tags"] for tag in ["fancy", "elegant", "stylish"])],
                    key=lambda x: x["score"],
                    reverse=True
                )
                fancy_bottoms = sorted(
                    [b for b in bottoms if any(tag in b["tags"] for tag in ["fancy", "elegant", "stylish"])],
                    key=lambda x: x["score"],
                    reverse=True
                )
                used_tops = set()
                used_bottoms = set()
                used_pairs = set()
                random.shuffle(fancy_tops)
                random.shuffle(fancy_bottoms)
                for top in fancy_tops:
                    if len(outfits) >= 3:
                        break
                    if top["id"] in used_tops:
                        continue
                    for bottom in fancy_bottoms:
                        if bottom["id"] in used_bottoms:
                            continue
                        combo_id = (top["id"], bottom["id"])
                        if combo_id in shown_combos or combo_id in used_pairs:
                            continue
                        color_score = self.calculate_color_harmony_score(top, bottom)
                        total_score = top["score"] + bottom["score"] + color_score
                        outfit_items = [top, bottom]
                        layer_added = False
                        best_layer = None
                        # Add layer if requested or needed
                        if ("layer" in required_kws or context["needs_layer"]) and layers:
                            best_layer = max(
                                [l for l in layers if "fancy" in l.get("tags", [])],
                                key=lambda x: x["score"],
                                default=None
                            )
                            if best_layer:
                                outfit_items.append(best_layer)
                                layer_added = True
                        outfits.append({
                            "type": "top+bottom" + ("+layer" if layer_added else ""),
                            "items": outfit_items,
                            "score": total_score + (best_layer["score"] if layer_added else 0),
                            "reason": f"Stylish {occasion.replace('_', ' ')} ensemble",
                            "color_harmony": self.get_color_harmony(outfit_items)
                        })
                        shown_combos.add(combo_id)
                        used_tops.add(top["id"])
                        used_bottoms.add(bottom["id"])
                        used_pairs.add(combo_id)
                        break  # Only one bottom per top

                # Fallback: if less than 3 outfits, fill with any valid top+bottom combos
                if len(outfits) < 3:
                    all_tops = [t for t in tops if t["id"] not in used_tops]
                    all_bottoms = [b for b in bottoms if b["id"] not in used_bottoms]
                    random.shuffle(all_tops)
                    random.shuffle(all_bottoms)
                    for top in all_tops:
                        if len(outfits) >= 3:
                            break
                        for bottom in all_bottoms:
                            combo_id = (top["id"], bottom["id"])
                            if combo_id not in shown_combos:
                                outfit_items = [top, bottom]
                                layer_added = False
                                best_layer = None
                                if ("layer" in required_kws or context["needs_layer"]) and layers:
                                    best_layer = max(
                                        [l for l in layers if "fancy" in l.get("tags", [])],
                                        key=lambda x: x["score"],
                                        default=None
                                    )
                                    if best_layer:
                                        outfit_items.append(best_layer)
                                        layer_added = True
                                outfits.append({
                                    "type": "top+bottom" + ("+layer" if layer_added else ""),
                                    "items": outfit_items,
                                    "score": top["score"] + bottom["score"] + (best_layer["score"] if layer_added else 0),
                                    "reason": f"{occasion.replace('_', ' ')} outfit",
                                    "color_harmony": self.get_color_harmony(outfit_items)
                                })
                                shown_combos.add(combo_id)
                                break  # Only one new combo per top

                context_key = f"{occasion}_{context['time']}_{context['weather']}"
                self.shown_combos_per_context[context_key] = shown_combos
                return outfits[:3]

    def assemble_outfits(self, matched_items, required_kws, preferred_kws, context, occasion):
        outfits = []
        context_key = f"{occasion}_{context['time']}_{context['weather']}"
        # Fix: ensure shown_combos is always a set, never None
        shown_combos = self.shown_combos_per_context.get(context_key)
        if shown_combos is None:
            shown_combos = set()
            self.shown_combos_per_context[context_key] = shown_combos

        # Prepare category lists for use in all branches
        tops = [item for item in matched_items if item["category"] == "topwear"]
        bottoms = [item for item in matched_items if item["category"] == "bottomwear"]
        layers = [item for item in matched_items if item["category"] == "layer"]
        one_pieces = [item for item in matched_items if item["category"] == "one_piece"]

        # SPECIAL HANDLING FOR PARTY/WEDDING/BEACH_PARTY/DATE OCCASIONS
        if occasion in ["party", "wedding", "beach_party", "date"]:
            # 1. Always include one one-piece (highest score)
            one_pieces_sorted = sorted(
                [op for op in one_pieces if any(t in op["tags"] for t in ["fancy", "elegant", "stylish"])],
                key=lambda x: x["score"],
                reverse=True
            )
            if one_pieces_sorted:
                op = one_pieces_sorted[0]
                combo_id = (op["id"],)
                if combo_id not in shown_combos:
                    outfits.append({
                        "type": "one_piece",
                        "items": [op],
                        "score": op["score"] * 1.2,
                        "reason": f"Elegant {occasion.replace('_', ' ')} one-piece",
                        "color_harmony": self.get_color_harmony([op])
                    })
                    shown_combos.add(combo_id)

            # 2. Add up to 2 top+bottom (+layer if needed/requested), all different sets
            fancy_tops = sorted(
                [t for t in tops if any(tag in t["tags"] for tag in ["fancy", "elegant", "stylish"])],
                key=lambda x: x["score"],
                reverse=True
            )
            fancy_bottoms = sorted(
                [b for b in bottoms if any(tag in b["tags"] for tag in ["fancy", "elegant", "stylish"])],
                key=lambda x: x["score"],
                reverse=True
            )
            used_tops = set()
            used_bottoms = set()
            used_pairs = set()
            random.shuffle(fancy_tops)
            random.shuffle(fancy_bottoms)
            for top in fancy_tops:
                if len(outfits) >= 3:
                    break
                if top["id"] in used_tops:
                    continue
                for bottom in fancy_bottoms:
                    if bottom["id"] in used_bottoms:
                        continue
                    combo_id = (top["id"], bottom["id"])
                    if combo_id in shown_combos or combo_id in used_pairs:
                        continue
                    color_score = self.calculate_color_harmony_score(top, bottom)
                    total_score = top["score"] + bottom["score"] + color_score
                    outfit_items = [top, bottom]
                    # Add layer if requested or needed
                    layer_added = False
                    if ("layer" in required_kws or context["needs_layer"]) and layers:
                        best_layer = max(
                            [l for l in layers if "fancy" in l.get("tags", [])],
                            key=lambda x: x["score"],
                            default=None
                        )
                        if best_layer:
                            outfit_items.append(best_layer)
                            layer_added = True
                    outfits.append({
                        "type": "top+bottom" + ("+layer" if layer_added else ""),
                        "items": outfit_items,
                        "score": total_score + (best_layer["score"] if layer_added else 0),
                        "reason": f"Stylish {occasion.replace('_', ' ')} ensemble",
                        "color_harmony": self.get_color_harmony(outfit_items)
                    })
                    shown_combos.add(combo_id)
                    used_tops.add(top["id"])
                    used_bottoms.add(bottom["id"])
                    used_pairs.add(combo_id)
                    break  # Only one bottom per top

            # Fallback: if less than 3 outfits, fill with any valid top+bottom combos
            if len(outfits) < 3:
                all_tops = [t for t in tops]
                all_bottoms = [b for b in bottoms]
                random.shuffle(all_tops)
                random.shuffle(all_bottoms)
                for top in all_tops:
                    for bottom in all_bottoms:
                        if len(outfits) >= 3:
                            break
                        combo_id = (top["id"], bottom["id"])
                        if combo_id not in shown_combos:
                            outfits.append({
                                "type": "top+bottom",
                                "items": [top, bottom],
                                "score": top["score"] + bottom["score"],
                                "reason": f"{occasion.replace('_', ' ')} outfit",
                                "color_harmony": self.get_color_harmony([top, bottom])
                            })
                            shown_combos.add(combo_id)
                            break  # Only one new combo per top

            self.shown_combos_per_context[context_key] = shown_combos
            return outfits[:3]

        self.shown_combos_per_context[context_key] = shown_combos
        return outfits[:1]  # Only one outfit (one-piece or fallback)

    def calculate_color_harmony_score(self, item1, item2):
        """Enhanced color scoring considering complements, analogs and fashion rules"""
        colors1 = [t for t in item1.get("tags", []) if t in self.color_complements]
        colors2 = [t for t in item2.get("tags", []) if t in self.color_complements]
        
        if not colors1 or not colors2:
            return 0
            
        # Check for complementary colors
        if any(c2 in self.color_complements.get(c1, []) for c1 in colors1 for c2 in colors2):
            return 25  # High score for complementary colors
        
        # Check for monochromatic
        if any(c1 == c2 for c1 in colors1 for c2 in colors2):
            return 20  # Good score for matching colors
        
        # Check for analogous colors (adjacent on color wheel)
        color_order = list(self.color_complements.keys())
        try:
            indices1 = [color_order.index(c) for c in colors1 if c in color_order]
            indices2 = [color_order.index(c) for c in colors2 if c in color_order]
            if indices1 and indices2:
                min_diff = min(abs(i1 - i2) for i1 in indices1 for i2 in indices2)
                if min_diff <= 2:  # Adjacent colors
                    return 15
        except ValueError:
            pass
        
        return 0  # No particular harmony

    def recommend_outfits(self, prompt):
        required_kws, preferred_kws, forbidden_kws = self.extract_keywords(prompt)
        context = self.get_context()
        occasion = self.analyze_occasion(prompt)
        
        matched_items = self.find_matching_items(required_kws, preferred_kws, forbidden_kws, context, occasion)
        outfits = self.assemble_outfits(matched_items, required_kws, preferred_kws, context, occasion)
        
        for outfit in outfits:
            for item in outfit["items"]:
                self.usage_history[item["id"]] = datetime.datetime.now()
        
        return {
            "type": "outfits",
            "items": outfits[:3],
            "context": context,
            "occasion": occasion
        }

    def recommend_outfits_fallback(self, occasion, context):
        """Generate emergency fallback recommendations when no matches are found"""
        # Get all items suitable for this occasion type, ignoring other criteria
        occasion_items = []
        for item in self.wardrobe_db:
            tags = item.get("tags", [])
            if occasion in tags:
                occasion_items.append(dict(item))
            elif item["category"] in ["topwear", "bottomwear"] and any(t in tags for t in ["formal", "casual", "versatile"]):
                occasion_items.append(dict(item))
        
        # For formal occasions, prioritize formal items
        if occasion in ["office", "interview", "business_meeting", "formal"]:
            formal_items = [i for i in occasion_items if any(t in i.get("tags", []) for t in ["formal", "office", "professional"])]
            if formal_items:
                occasion_items = formal_items
        
        # For casual occasions, prioritize casual items
        if occasion in ["casual", "picnic", "shopping"]:
            casual_items = [i for i in occasion_items if "casual" in i.get("tags", [])]
            if casual_items:
                occasion_items = casual_items
        
        # Generate some outfits
        tops = [i for i in occasion_items if i["category"] == "topwear"]
        bottoms = [i for i in occasion_items if i["category"] == "bottomwear"]
        one_pieces = [i for i in occasion_items if i["category"] == "one_piece"]
        
        # Assign arbitrary scores
        for item in occasion_items:
            item["score"] = 50
        
        # Build outfits (one from each category if available)
        outfits = []
        
        # Add a one-piece option if available
        if one_pieces:
            outfits.append({
                "type": "one_piece",
                "items": [random.choice(one_pieces)],
                "score": 50.0,
                "reason": f"Emergency fallback for {occasion}",
                "color_harmony": self.get_color_harmony([one_pieces[0]])
            })
        
        # Add top+bottom options
        if tops and bottoms:
            used_tops = set()
            used_bottoms = set()
            
            for _ in range(min(3, len(tops), len(bottoms))):
                top = random.choice([t for t in tops if t["id"] not in used_tops])
                bottom = random.choice([b for b in bottoms if b["id"] not in used_bottoms])
                
                outfits.append({
                    "type": "top+bottom",
                    "items": [top, bottom],
                    "score": 50.0,
                    "reason": f"Emergency fallback for {occasion}",
                    "color_harmony": self.get_color_harmony([top, bottom])
                })
                
                used_tops.add(top["id"])
                used_bottoms.add(bottom["id"])
                
                if len(outfits) >= 3:
                    break
        
        # Final fallback: add single items from each category if still not enough outfits
        if len(outfits) < 3:
            categories = ["topwear", "bottomwear", "one_piece", "layer"]
            for category in categories:
                items = [i for i in self.wardrobe_db if i["category"] == category]
                if items:
                    # Pick the highest scored item or just the first one if scores are not set
                    item = items[0]
                    # Avoid adding duplicates
                    already_used = any(item["id"] in [x["id"] for o in outfits for x in o["items"]])
                    if not already_used:
                        outfits.append({
                            "type": category,
                            "items": [item],
                            "score": 40.0,
                            "reason": f"Emergency fallback single {category}",
                            "color_harmony": self.get_color_harmony([item])
                        })
                    if len(outfits) >= 3:
                        break

        return outfits[:3]

    def generate_outfit_html(self, outfits, filename="outfits.html"):
        html = [
            "<!DOCTYPE html>",
            "<html><head>",
            "<title>Outfit Recommendations</title>",
            "<style>",
            "body { font-family: Arial, sans-serif; padding: 20px; }",
            ".outfit { border: 1px solid #ddd; padding: 15px; margin-bottom: 20px; }",
            ".outfit-flex { display: flex; flex-direction: row; align-items: flex-start; gap: 40px; }",
            ".outfit-details { min-width: 250px; max-width: 350px; }",
            ".vertical-stack { display: flex; flex-direction: column; align-items: center; gap: 20px; }",
            ".layer-under { display: flex; flex-direction: column; align-items: center; margin-top: 30px; }",
            ".side-info { display: flex; flex-direction: column; gap: 30px; justify-content: flex-start; }",
            ".item { margin: 10px; text-align: center; }",
            ".layer-img { margin-top: 10px; border-top: 1px solid #eee; padding-top: 10px; }",
            "img { max-width: 150px; }",
        ]
        html.append("</style></head><body>")
        html.append("<h1>Recommended Outfits</h1>")
        if not outfits:
            html.append("<p>No outfits found for your request. Try a different prompt or check your wardrobe data.</p>")
        else:
            for idx, outfit in enumerate(outfits, 1):
                html.append(f'<div class="outfit"><div class="outfit-flex">')
                # Outfit details on the left
                html.append('<div class="outfit-details">')
                html.append(f'<h2>Outfit {idx}</h2>')
                html.append(f'<p>Score: {outfit["score"]:.1f} - {outfit.get("reason", "")}</p>')
                html.append(f'<p>Color Harmony: {outfit.get("color_harmony", "")}</p>')
                # Side info for each item except layer
                html.append('<div class="side-info">')
                top = None
                bottom = None
                layer = None
                others = []
                for item in outfit["items"]:
                    if item["category"] == "topwear":
                        top = item
                    elif item["category"] == "bottomwear":
                        bottom = item
                    elif item["category"] == "layer":
                        layer = item
                    else:
                        others.append(item)
                if top:
                    html.append(
                        f'<div><b>{top["name"]}</b> ({top["category"]})<br>'
                        f'ID: {top["id"]}<br>'
                        f'Tags: {", ".join(top["tags"])}</div>'
                    )
                if bottom:
                    html.append(
                        f'<div><b>{bottom["name"]}</b> ({bottom["category"]})<br>'
                        f'ID: {bottom["id"]}<br>'
                        f'Tags: {", ".join(bottom["tags"])}</div>'
                    )
                for item in others:
                    html.append(
                        f'<div><b>{item["name"]}</b> ({item["category"]})<br>'
                        f'ID: {item["id"]}<br>'
                        f'Tags: {", ".join(item["tags"])}</div>'
                    )
                html.append('</div>')  # end side-info
                html.append('</div>')  # end outfit-details

                # Main outfit images (topwear above bottomwear, stacked vertically)
                html.append('<div class="vertical-stack">')
                if top:
                    html.append(
                        f'<div class="item">'
                        f'<img src="static/{top.get("image", "")}" alt="{top["name"]}">'
                        f'</div>'
                    )
                if bottom:
                    html.append(
                        f'<div class="item">'
                        f'<img src="static/{bottom.get("image", "")}" alt="{bottom["name"]}">'
                        f'</div>'
                    )
                # Any other (e.g. one_piece)
                for item in others:
                    html.append(
                        f'<div class="item">'
                        f'<img src="static/{item.get("image", "")}" alt="{item["name"]}">'
                        f'</div>'
                    )
                # Layer under the stack if present
                if layer:
                    html.append(
                        f'<div class="item layer-img">'
                        f'<img src="static/{layer.get("image", "")}" alt="{layer["name"]}"><br>'
                        f'{layer["name"]} ({layer["category"]})<br>'
                        f'ID: {layer["id"]}<br>'
                        f'Tags: {", ".join(layer["tags"])}'
                        f'</div>'
                    )
                html.append('</div>')  # end vertical-stack
                html.append('</div></div>')  # end outfit-flex and outfit
        html.append("</body></html>")
        with open(filename, "w") as f:
            f.write("\n".join(html))
        return os.path.abspath(filename)

    def get_context_key(self, occasion, required_kws):
        # Use occasion and first required color as context key
        color = None
        for kw in required_kws:
            if kw in self.color_complements:
                color = kw
                break
        return (occasion, color or "")

def print_outfits(result, recommender=None):
    print(f"\nContext: Time: {result['context']['time']}, Weather: {result['context']['weather']}")
    print(f"Occasion: {result['occasion'].replace('_', ' ').title()}")
    
    if not result["items"]:
        print("\nNo exact matches found for your criteria. Here are some alternative suggestions:")
        # Generate emergency fallback recommendations
        fallback_results = recommender.recommend_outfits_fallback(result["occasion"], result["context"])
        for idx, outfit in enumerate(fallback_results, 1):
            print(f"\nOutfit {idx} (Score: {outfit['score']:.1f}) - {outfit.get('reason', 'Fallback Option')}")
            print("Items:")
            for item in outfit["items"]:
                print(f"  - {item['name']} ({item['category']})")
                print(f"    ID: {item['id']}")
                print(f"    Tags: {', '.join(item['tags'])}")
            if outfit.get('color_harmony'):
                print(f"Color Harmony: {outfit['color_harmony']}")
        if recommender:
            html_path = recommender.generate_outfit_html(fallback_results, filename="outfits.html")
            print(f"\nVisualize these outfits: file://{html_path}")
            webbrowser.open(f'file://{html_path}')
    else:
        for idx, outfit in enumerate(result["items"], 1):
            print(f"\nOutfit {idx} (Score: {outfit['score']:.1f}) - {outfit.get('reason', 'Outfit')}")
            print("Items:")
            for item in outfit["items"]:
                print(f"  - {item['name']} ({item['category']})")
                print(f"    ID: {item['id']}")
                print(f"    Tags: {', '.join(item['tags'])}")
            if outfit.get('color_harmony'):
                print(f"Color Harmony: {outfit['color_harmony']}")
        if recommender:
            html_path = recommender.generate_outfit_html(result["items"], filename="outfits.html")
            print(f"\nVisualize these outfits: file://{html_path}")
            webbrowser.open(f'file://{html_path}')

if __name__ == "__main__":
    recommender = SmartOutfitRecommender()
    print("Smart Outfit Recommender")
    print("-----------------------")
    print("Enter your outfit request (e.g. 'gym outfit in green')")
    while True:
        prompt = input("\nWhat would you like to wear today? ").strip()
        if prompt.lower() in ['exit', 'quit']:
            break
        result = recommender.recommend_outfits(prompt)
        print_outfits(result, recommender)
        if result["items"]:
            try:
                choice = input("Select outfit to save preferences (1-3) or Enter to skip: ")
                if choice.isdigit():
                    idx = int(choice) - 1
                    if 0 <= idx < len(result["items"]):
                        recommender.update_user_preferences(result["items"][idx])
                        print("Preferences updated!")
            except Exception as e:
                print(f"Error: {e}")
