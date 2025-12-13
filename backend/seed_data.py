import asyncio
import sys
import os

from database import engine, Base, SessionLocal
from models import User, Category, Product, Brand, StoreLocation, SiteSetting
from auth import get_password_hash
from sqlalchemy import select

async def seed_data():
    print("🔄 Connecting to database...")
    async with engine.begin() as conn:
        print("🗑️  Dropping existing tables...")
        await conn.run_sync(Base.metadata.drop_all)
        print("✨ Creating new tables...")
        await conn.run_sync(Base.metadata.create_all)

    async with SessionLocal() as db:
        # Check if already seeded
        result = await db.execute(select(User))
        if result.scalars().first():
            print("✅ Database already seeded!")
            return

        print("🌱 Seeding data...")
        
        print("👤 Creating Admin User...")
        # Create Admin
        admin = User(username="admin", hashed_password=get_password_hash("admin"), is_admin=True)
        db.add(admin)

        print("🏷️  Creating Luxury Brands...")
        # Create Brands
        brands_data = [
            ("Cartier", "https://upload.wikimedia.org/wikipedia/commons/3/31/Cartier_logo.svg"),
            ("Tiffany & Co.", "https://upload.wikimedia.org/wikipedia/commons/0/05/Tiffany_and_Co.svg"),
            ("Bulgari", "https://upload.wikimedia.org/wikipedia/commons/3/30/Bulgari_logo.svg"),
            ("Van Cleef & Arpels", "https://upload.wikimedia.org/wikipedia/en/8/8f/Van_Cleef_%26_Arpels_logo.svg"),
            ("Graff", "https://upload.wikimedia.org/wikipedia/commons/e/e6/Graff_Diamonds_logo.svg"),
            ("Rolex", "https://upload.wikimedia.org/wikipedia/commons/5/54/Rolex_logo.svg"),
            ("Omega", "https://upload.wikimedia.org/wikipedia/commons/f/f6/Omega_Logo.svg"),
            ("Patek Philippe", "https://upload.wikimedia.org/wikipedia/en/thumb/f/f0/Patek_Philippe_SA_logo.svg/1200px-Patek_Philippe_SA_logo.svg.png"),
            ("Audemars Piguet", "https://upload.wikimedia.org/wikipedia/en/thumb/5/52/Audemars_Piguet_logo.svg/1200px-Audemars_Piguet_logo.svg.png"),
            ("Hermès", "https://upload.wikimedia.org/wikipedia/commons/8/82/Herm%C3%A8s_Logo.svg"),
            ("Chanel", "https://upload.wikimedia.org/wikipedia/en/9/92/Chanel_logo_interlocking_cs.svg"),
            ("Gucci", "https://upload.wikimedia.org/wikipedia/commons/7/79/Gucci_Logo.svg"),
            ("Louis Vuitton", "https://upload.wikimedia.org/wikipedia/commons/c/c4/Louis_Vuitton_LV_logo.png"),
            ("Dior", "https://upload.wikimedia.org/wikipedia/en/thumb/1/11/Dior_Logo.svg/1200px-Dior_Logo.svg.png"),
            ("Chopard", "https://upload.wikimedia.org/wikipedia/en/thumb/4/42/Chopard_Logo.svg/1200px-Chopard_Logo.svg.png"),
            ("Breguet", "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Breguet_logo.svg/1200px-Breguet_logo.svg.png"),
        ]
        
        created_brands = {}
        for name, logo in brands_data:
            b = Brand(name=name, logo_url=logo)
            db.add(b)
            created_brands[name] = b
            
        await db.flush()

        print("📂 Creating Categories...")
        # Create Categories
        categories_data = [
            ("Necklaces", "https://images.unsplash.com/photo-1599643478518-17488fbbcd75?w=400"),
            ("Rings", "https://images.unsplash.com/photo-1605100804763-ebea24b87258?w=400"),
            ("Earrings", "https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?w=400"),
            ("Bracelets", "https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=400"),
            ("Watches", "https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=400"),
            ("Pendants", "https://images.unsplash.com/photo-1601121141461-9d660d2b4b60?w=400"),
            ("Sets", "https://images.unsplash.com/photo-1579737158914-1e05d04cc634?w=400"),
            ("Anklets", "https://images.unsplash.com/photo-1630019852942-f89202989a51?w=400"),
            ("Cufflinks", "https://images.unsplash.com/photo-1617038224538-4b711e6498bd?w=400"),
            ("Brooches", "https://images.unsplash.com/photo-1616857943507-6f8d8cabd704?w=400"),
            ("Charms", "https://images.unsplash.com/photo-1611085583191-a3b181a88401?w=400"),
            ("Chokers", "https://images.unsplash.com/photo-1573408301185-9146fe634ad0?w=400"),
            ("Tiaras", "https://images.unsplash.com/photo-1546167889-0b4f5ff52bc6?w=400"),
            ("Body Jewelry", "https://images.unsplash.com/photo-1629224316810-9d8805b95076?w=400"),
            ("Wedding Bands", "https://images.unsplash.com/photo-1603561596112-0a132b72231d?w=400"),
        ]

        created_cats = {}
        for name, img in categories_data:
            c = Category(name=name, image_url=img)
            db.add(c)
            created_cats[name] = c
            
        await db.flush()

        print("💎 Creating Premium Jewelry Products...")
        # Create Products - LUXURY JEWELRY CATALOG
        products = [
            # NECKLACES
            Product(
                name="Panthère de Cartier Necklace",
                description="Panthère de Cartier necklace, 18K yellow gold, set with 2 emeralds and 19 brilliant-cut diamonds totaling 0.11 carats. Onyx.",
                price=16500.00,
                stock=5,
                image_url="https://images.unsplash.com/photo-1599643477877-5317429188d3?w=600",
                specs={"Material": "18K Yellow Gold", "Gemstone": "Emeralds, Diamonds, Onyx", "Collection": "Panthère", "Chain Length": "45 cm"},
                rating=5.0,
                review_count=124,
                category_id=created_cats["Necklaces"].id,
                brand_id=created_brands["Cartier"].id
            ),
            Product(
                name="Vintage Alhambra Necklace 10 Motifs",
                description="Faithful to the very first Alhambra jewel created in 1968, the Vintage Alhambra creations by Van Cleef & Arpels are distinguished by their unique, timeless elegance.",
                price=8900.00,
                stock=12,
                image_url="https://images.unsplash.com/photo-1600860888258-0cb934d4007b?w=600",
                specs={"Material": "18K Yellow Gold", "Gemstone": "Mother-of-pearl", "Motifs": "10", "Clasp": "Hallmark clasp"},
                rating=4.9,
                review_count=452,
                category_id=created_cats["Necklaces"].id,
                brand_id=created_brands["Van Cleef & Arpels"].id
            ),
            Product(
                name="Graff Butterfly Silhouette Necklace",
                description="Capturing the delicate flight of a butterfly, this diamond necklace features an openwork silhouette illuminated by pavé diamonds.",
                price=18500.00,
                stock=3,
                image_url="https://images.unsplash.com/photo-1515562141207-7a88fb05220c?w=600",
                specs={"Material": "White Gold", "Gemstone": "Diamond", "Collection": "Butterfly", "Carat": "0.55 ct"},
                rating=5.0,
                review_count=28,
                category_id=created_cats["Necklaces"].id,
                brand_id=created_brands["Graff"].id
            ),
            Product(
                name="Divas' Dream Necklace",
                description="Inspired by feminine elegance and the enchanting allure of the eternal city, the Divas' Dream necklace pays homage to the most glamorous divas.",
                price=4200.00,
                stock=8,
                image_url="https://images.unsplash.com/photo-1601121141461-9d660d2b4b60?w=600",
                specs={"Material": "18K Rose Gold", "Gemstone": "Carnelian, Diamond", "Collection": "Divas' Dream"},
                rating=4.8,
                review_count=156,
                category_id=created_cats["Necklaces"].id,
                brand_id=created_brands["Bulgari"].id
            ),
            Product(
                name="Tiffany T Smile Pendant",
                description="Graphic angles and clean lines blend to create the beautiful clarity of the Tiffany T collection.",
                price=1200.00,
                stock=50,
                image_url="https://images.unsplash.com/photo-1610484738743-4a6c67d34200?w=600",
                specs={"Material": "18K Rose Gold", "Size": "Small", "Collection": "Tiffany T"},
                rating=4.7,
                review_count=890,
                category_id=created_cats["Necklaces"].id,
                brand_id=created_brands["Tiffany & Co."].id
            ),
            
            # RINGS
            Product(
                name="Tiffany Setting Engagement Ring",
                description="The ring of the rings, as it has been called, the Tiffany® Setting is the world’s most iconic engagement ring.",
                price=45000.00,
                stock=3,
                image_url="https://images.unsplash.com/photo-1605100804763-ebea24b87258?w=600",
                specs={"Material": "Platinum", "Gemstone": "Diamond", "Carat": "2.5 ct", "Cut": "Round Brilliant"},
                rating=4.9,
                review_count=890,
                category_id=created_cats["Rings"].id,
                brand_id=created_brands["Tiffany & Co."].id
            ),
            Product(
                name="B.Zero1 Ring",
                description="Drawing its inspiration from the most renowned amphitheater of the world, the Colosseum, the B.zero1 ring is a true statement of Bulgari’s creative vision.",
                price=2850.00,
                stock=25,
                image_url="https://images.unsplash.com/photo-1629224316810-9d8805b95076?w=600",
                specs={"Material": "18K Rose Gold", "Collection": "B.Zero1", "Width": "4-band", "Made In": "Italy"},
                rating=4.8,
                review_count=210,
                category_id=created_cats["Rings"].id,
                brand_id=created_brands["Bulgari"].id
            ),
            Product(
                name="Graff Icon Round Diamond Family",
                description="A celebration of the beautiful silhouette of a round brilliant diamond, the Icon setting is a house signature.",
                price=125000.00,
                stock=1,
                image_url="https://images.unsplash.com/photo-1603561596112-0a132b7223de?w=600",
                specs={"Material": "White Gold", "Gemstone": "Diamond", "Carat": "5.0 ct", "Clarity": "FL"},
                rating=5.0,
                review_count=12,
                category_id=created_cats["Rings"].id,
                brand_id=created_brands["Graff"].id
            ),
            Product(
                name="Juste un Clou Ring",
                description="Designed in 1970s New York, the Juste un Clou collection reflects a wild, freewheeling era. Bold, modern, and innovative.",
                price=2450.00,
                stock=18,
                image_url="https://images.unsplash.com/photo-1622398925373-3f9162e39c56?w=600",
                specs={"Material": "18K Yellow Gold", "Collection": "Juste un Clou", "Width": "2.65mm"},
                rating=4.7,
                review_count=334,
                category_id=created_cats["Rings"].id,
                brand_id=created_brands["Cartier"].id
            ),
            Product(
                name="Perlée Pearls of Gold Ring",
                description="The Perlée pearls of gold creations are characterized by the delicate interplay of gold beads.",
                price=1800.00,
                stock=15,
                image_url="https://images.unsplash.com/photo-1598560976739-9698b6f400c9?w=600",
                specs={"Material": "18K White Gold", "Collection": "Perlée", "Size": "Medium model"},
                rating=4.9,
                review_count=190,
                category_id=created_cats["Rings"].id,
                brand_id=created_brands["Van Cleef & Arpels"].id
            ),

            # EARRINGS
            Product(
                name="Tiffany HardWear Link Earrings",
                description="Inspired by the bold architecture and edge of New York City, Tiffany HardWear combines gauge links and industrial shapes.",
                price=1900.00,
                stock=30,
                image_url="https://images.unsplash.com/photo-1635767798638-3e2523422dc0?w=600",
                specs={"Material": "18K Gold", "Collection": "Tiffany HardWear", "Style": "Drop", "Weight": "Heavy"},
                rating=4.7,
                review_count=320,
                category_id=created_cats["Earrings"].id,
                brand_id=created_brands["Tiffany & Co."].id
            ),
            Product(
                name="Serpenti Viper Earrings",
                description="A tribute to the spirit of the serpent, capturing the power of seduction in each curve.",
                price=7600.00,
                stock=10,
                image_url="https://images.unsplash.com/photo-1615655114865-4cc1bda5901e?w=600",
                specs={"Material": "18K Rose Gold", "Gemstone": "Demi-pavé Diamonds", "Collection": "Serpenti", "Weight": "8.5g"},
                rating=4.9,
                review_count=156,
                category_id=created_cats["Earrings"].id,
                brand_id=created_brands["Bulgari"].id
            ),
            Product(
                name="Wild Flower Diamond Earrings",
                description="A joyful celebration of the English garden, re-created in diamonds that grow in abundance.",
                price=15000.00,
                stock=4,
                image_url="https://images.unsplash.com/photo-1630019862942-f89202989a51?w=600",
                specs={"Material": "White Gold", "Gemstone": "Diamond", "Collection": "Wild Flower", "Carat": "1.34 ct"},
                rating=5.0,
                review_count=42,
                category_id=created_cats["Earrings"].id,
                brand_id=created_brands["Graff"].id
            ),
            Product(
                name="Trinity Earrings",
                description="Trinity is the perfect connection, founded on an interplay of rose gold, yellow gold and white gold.",
                price=2100.00,
                stock=22,
                image_url="https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?w=600",
                specs={"Material": "18K White, Rose, Yellow Gold", "Collection": "Trinity", "Width": "3.3mm"},
                rating=4.8,
                review_count=560,
                category_id=created_cats["Earrings"].id,
                brand_id=created_brands["Cartier"].id
            ),
            Product(
                name="Vintage Alhambra Earrings",
                description="Faithful to the very first Alhambra jewel created in 1968, the Vintage Alhambra creations are a symbol of luck.",
                price=4500.00,
                stock=9,
                image_url="https://images.unsplash.com/photo-1598560977823-38d58c148fd4?w=600",
                specs={"Material": "18K Yellow Gold", "Gemstone": "Onyx", "Collection": "Alhambra"},
                rating=4.9,
                review_count=312,
                category_id=created_cats["Earrings"].id,
                brand_id=created_brands["Van Cleef & Arpels"].id
            ),

            # BRACELETS
            Product(
                name="Cartier Love Bracelet",
                description="A child of 1970s New York, the LOVE collection remains today an iconic symbol of love that transgresses convention.",
                price=7350.00,
                stock=40,
                image_url="https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=600",
                specs={"Material": "18K Yellow Gold", "Width": "6.1mm", "Screwdriver": "Included", "Size": "17"},
                rating=4.8,
                review_count=2300,
                category_id=created_cats["Bracelets"].id,
                brand_id=created_brands["Cartier"].id
            ),
            Product(
                name="Perlée Clovers Bracelet",
                description="Joyful and feminine, the Perlée™ clovers jewelry creations are adorned with precious clover motifs.",
                price=14500.00,
                stock=8,
                image_url="https://images.unsplash.com/photo-1573408301185-9146fe634ad0?w=600",
                specs={"Material": "18K White Gold", "Gemstone": "Diamonds", "Diamond Quality": "DEF, IF to VVS", "Size": "Small"},
                rating=5.0,
                review_count=89,
                category_id=created_cats["Bracelets"].id,
                brand_id=created_brands["Van Cleef & Arpels"].id
            ),
            Product(
                name="Tiffany T Wire Bracelet",
                description="As multifaceted as it is iconic, the Tiffany T collection is a tangible reminder of the connections we feel but can't always see.",
                price=2600.00,
                stock=15,
                image_url="https://images.unsplash.com/photo-1610484738743-4a6c67d34200?w=600",
                specs={"Material": "18K Rose Gold", "Collection": "Tiffany T", "Size": "Medium"},
                rating=4.7,
                review_count=450,
                category_id=created_cats["Bracelets"].id,
                brand_id=created_brands["Tiffany & Co."].id
            ),
            Product(
                name="Serpenti Viper Bracelet",
                description="An ultra-modern interpretation of Bvlgari’s celebrated icon of glamour and seduction, Serpenti Viper enchants with its innovative geometric design.",
                price=6800.00,
                stock=7,
                image_url="https://images.unsplash.com/photo-1614768393529-57ad214a79db?w=600",
                specs={"Material": "18K White Gold", "Collection": "Serpenti", "Size": "M"},
                rating=4.9,
                review_count=98,
                category_id=created_cats["Bracelets"].id,
                brand_id=created_brands["Bulgari"].id
            ),
            Product(
                name="Lawrence Graff Signature Bracelet",
                description="A striking, contemporary bangle featuring the angular facets that are the hallmark of the collection.",
                price=9000.00,
                stock=6,
                image_url="https://images.unsplash.com/photo-1512163143273-bde0e3cc5409?w=600",
                specs={"Material": "Rose Gold", "Gemstone": "Diamond", "Collection": "Lawrence Graff Signature"},
                rating=4.8,
                review_count=45,
                category_id=created_cats["Bracelets"].id,
                brand_id=created_brands["Graff"].id
            ),

            # WATCHES
            Product(
                name="Rolex Day-Date 40",
                description="The Oyster Perpetual Day-Date 40 in 18 ct yellow gold with a white dial, fluted bezel and a President bracelet.",
                price=41500.00,
                stock=5,
                image_url="https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=600",
                specs={"Material": "18K Yellow Gold", "Movement": "Perpetual, mechanical, self-winding", "Calibre": "3255", "Water Resistance": "100m"},
                rating=4.9,
                review_count=670,
                category_id=created_cats["Watches"].id,
                brand_id=created_brands["Rolex"].id
            ),
            Product(
                name="Cartier Tank Must Watch",
                description="Tank Must watch, extra-large model, mechanical movement with automatic winding. Steel case.",
                price=4900.00,
                stock=15,
                image_url="https://images.unsplash.com/photo-1522312346375-d1a52e2b99b3?w=600",
                specs={"Material": "Steel", "Movement": "Automatic", "Strap": "Black Calfskin", "Water Resistance": "3 bar"},
                rating=4.7,
                review_count=342,
                category_id=created_cats["Watches"].id,
                brand_id=created_brands["Cartier"].id
            ),
            Product(
                name="Nautilus 5711/1A",
                description="With the rounded octagonal shape of its bezel, the ingenious porthole construction of its case, and its horizontally embossed dial, the Nautilus has epitomized the elegant sports watch since 1976.",
                price=135000.00,
                stock=1,
                image_url="https://images.unsplash.com/photo-1523170335258-f5ed11844a49?w=600",
                specs={"Material": "Stainless Steel", "Movement": "Self-winding", "Dial": "Blue", "Water Resistance": "120m"},
                rating=5.0,
                review_count=1200,
                category_id=created_cats["Watches"].id,
                brand_id=created_brands["Patek Philippe"].id
            ),
            Product(
                name="Royal Oak Selfwinding",
                description="The Royal Oak is recognizable by its octagonal bezel secured by 8 hexagonal screws.",
                price=45000.00,
                stock=3,
                image_url="https://images.unsplash.com/photo-1619159981242-426c11bc3342?w=600",
                specs={"Material": "Stainless Steel", "Movement": "Self-winding", "Dial": "Grande Tapisserie", "Size": "41mm"},
                rating=4.9,
                review_count=890,
                category_id=created_cats["Watches"].id,
                brand_id=created_brands["Audemars Piguet"].id
            ),
            Product(
                name="Speedmaster Moonwatch Professional",
                description="The Speedmaster Moonwatch is one of the world's most iconic timepieces. Having been a part of all six lunar missions, the legendary chronograph is an impressive representation of the brand's adventurous pioneering spirit.",
                price=7500.00,
                stock=20,
                image_url="https://images.unsplash.com/photo-1623998021446-45cd96e3529a?w=600",
                specs={"Material": "Steel", "Movement": "Manual-winding", "Calibre": "3861", "Water Resistance": "50m"},
                rating=4.8,
                review_count=2100,
                category_id=created_cats["Watches"].id,
                brand_id=created_brands["Omega"].id
            )
        ]
        db.add_all(products)

        print("📍 Creating Store Locations...")
        # Create Store Locations
        stores = [
            StoreLocation(
                name="Maison El Wali - Dubai Mall",
                address="Fashion Avenue, Ground Floor",
                city="Dubai, UAE",
                latitude=25.1972,
                longitude=55.2744,
                phone="+971 4 555 0199"
            ),
            StoreLocation(
                name="Maison El Wali - Paris",
                address="12 Place Vendôme",
                city="Paris, France",
                latitude=48.8674,
                longitude=2.3294,
                phone="+33 1 55 55 01 23"
            ),
            StoreLocation(
                name="Maison El Wali - New York",
                address="727 Fifth Avenue",
                city="New York, NY",
                latitude=40.7624,
                longitude=-73.9739,
                phone="+1 212 555 0456"
            ),
            StoreLocation(
                name="Maison El Wali - London",
                address="15 New Bond Street",
                city="London, UK",
                latitude=51.5114,
                longitude=-0.1428,
                phone="+44 20 7555 0789"
            ),
        ]
        db.add_all(stores)

        print("⚙️  Creating Site Settings...")
        # Create Site Settings
        settings_data = [
            ("store_name", "MAISON EL WALI"),
            ("hero_title", "Discover The Art<br>Of Elegance"),
            ("hero_subtitle", "Curated selection of premium gold and diamond jewelry. Visit our showrooms to experience true luxury."),
            ("hero_badge", "✨ Timeless Jewelry Collection 2025"),
            ("contact_email", "concierge@maisonelwali.com"),
            ("contact_phone", "+971 4 123 4567"),
            ("contact_address", "Dubai Mall, Fashion Avenue"),
            ("theme_primary", "#D4AF37"),
            ("theme_secondary", "#1F2937"),
            ("theme_accent", "#F59E0B"),
            ("theme_font_family", "")
        ]
        
        settings = [SiteSetting(key=key, value=value) for key, value in settings_data]
        db.add_all(settings)
        
        await db.commit()
        print("✅ Database successfully seeded with MAISON EL WALI Luxury Collection!")
        print(f"   - {len(products)} Jewelry Items")
        print(f"   - {len(stores)} Global Boutiques")
        print(f"   - {len(settings)} Site Settings")
        print(f"   - Admin User Created (admin/admin)")

if __name__ == "__main__":
    asyncio.run(seed_data())
