from models.model import Category, Cart, Product, CartProduct

categories_json = {
    'Phones': {
        'Stationary': {
            'Panasonic': {},
            'VTech': {}
        },
        'Mobile': {
            'Samsung': {},
            'Xiaomi': {},
        }
    },
    'Cpu': {
        'Intel': {},
        'AMD': {}
    }
}

categories_description_dict = {
    'Phones': 'Category of Phones',
    'Stationary': 'Stationary DECT phones',
    'Panasonic': 'Category of Panasonic stationary phones',
    'VTech': 'Category of VTech stationary phones',
    'Mobile': 'Mobile phones',
    'Samsung': 'Samsung phones',
    'Xiaomi': 'Xiaomi phones',
    'Cpu': "Category of cpu's",
    'Intel': "Category of Intel cpu's",
    'AMD': "Category of AMD cpu's"
}


def get_cat_id(cat_name):
    return str(Category.objects(title=cat_name).get().id)


products_dict = {
    'Panasonic_1': {
        'title': 'Panasonic KX-TGE43B',
        'category': 'Panasonic',
        'img_url': 'https://shop.panasonic.com/dw/image/v2/AASQ_PRD/on/demandware.static/-/Sites-shop-pna-master-catalog/default/dw5cbc0768/product/images/KX-TGE432B_ALT01.jpg?sw=1000&sh=1000&sm=fit',
        'article': 'KX-TGE43B',
        'description': 'Expandable Cordless Phone System with Answering Machine ',
        'price': 6995,
        'in_stock': 100,
    },
    'Panasonic_2': {
        'title': 'Panasonic KX-TGE434B',
        'category': 'Panasonic',
        'img_url': 'https://shop.panasonic.com/dw/image/v2/AASQ_PRD/on/demandware.static/-/Sites-shop-pna-master-catalog/default/dw28e2f194/product/images/KX-TGE434B_ALT01.jpg?sw=1000&sh=1000&sm=fit',
        'article': 'KX-TGE434B',
        'description': 'Expandable Cordless Phone System with Answering Machine - 4 Handsets - KX-TGE434B',
        'price': 10995,
        'in_stock': 100,
    },
    'Panasonic_3': {
        'title': 'Panasonic KX-TGE484S2',
        'category': 'Panasonic',
        'img_url': 'https://shop.panasonic.com/dw/image/v2/AASQ_PRD/on/demandware.static/-/Sites-shop-pna-master-catalog/default/dw9bbcb2aa/product/images/KX-TGE484S2_ALT01.jpg?sw=1000&sh=1000&sm=fit',
        'article': 'KX-TGE484S2',
        'description': 'Link2Cell Bluetooth® Cordless Phone with Rugged Phone - 4 Handsets - KX-TGE484S2',
        'price': 15995,
        'in_stock': 100
    },
    'Panasonic_4': {
        'title': 'Panasonic KX-TGC364B',
        'category': 'Panasonic',
        'img_url': 'https://shop.panasonic.com/dw/image/v2/AASQ_PRD/on/demandware.static/-/Sites-shop-pna-master-catalog/default/dw514ecc76/product/images/KX-TGC364B_ALT01.jpg?sw=1000&sh=1000&sm=fit',
        'article': 'KX-TGC364B',
        'description': 'Expandable Cordless Phone with Answering System - 4 Handsets - KX-TGC364B',
        'price': 8995,
        'in_stock': 100,
    },
    'Panasonic_5': {
        'title': 'Panasonic KX-TGD583M2',
        'category': 'Panasonic',
        'img_url': 'https://shop.panasonic.com/dw/image/v2/AASQ_PRD/on/demandware.static/-/Sites-shop-pna-master-catalog/default/dw3f203db1/product/images/KX-TGD583M2_ALT01.jpg?sw=1000&sh=1000&sm=fit',
        'article': 'KX-TGD583M2',
        'description': 'Link2Cell Bluetooth® Cordless Phone with Voice Assist and Answering Machine Standard Handset + Rugged Phone Series - KX-TGD58M2',
        'price': 11995,
        'in_stock': 100,
    },
    'Panasonic_6': {
        'title': 'Panasonic KX-TGD563M',
        'category': 'Panasonic',
        'img_url': 'https://shop.panasonic.com/dw/image/v2/AASQ_PRD/on/demandware.static/-/Sites-shop-pna-master-catalog/default/dw79cd4bc1/product/images/KX-TGD563M_ALT01.jpg?sw=1000&sh=1000&sm=fit',
        'article': 'KX-TGD563M',
        'description': 'Link2Cell Bluetooth® Cordless Phone with Voice Assist and Answering Machine - KX-TGD56M Series',
        'price': 10995,
        'in_stock': 100,
    },
    'Panasonic_7': {
        'title': 'Panasonic KX-TGD562G',
        'category': 'Panasonic',
        'img_url': 'https://shop.panasonic.com/dw/image/v2/AASQ_PRD/on/demandware.static/-/Sites-shop-pna-master-catalog/default/dwf346bfce/product/images/KX-TGD562G_ALT01.jpg?sw=1000&sh=1000&sm=fit',
        'article': 'KX-TGD562G',
        'description': 'Link2Cell Bluetooth Cordless Phone with Answering Machine - KX-TGD56 Series',
        'price': 8995,
        'in_stock': 100,
    },
    'Panasonic_8': {
        'title': 'Panasonic KX-TGD510B',
        'category': 'Panasonic',
        'img_url': 'https://shop.panasonic.com/dw/image/v2/AASQ_PRD/on/demandware.static/-/Sites-shop-pna-master-catalog/default/dw8dd73474/product/images/KX-TGD510B_ALT01.jpg?sw=1000&sh=1000&sm=fit',
        'article': 'KX-TGD510B',
        'description': 'Expandable Cordless Phone with Call Block - KX-TGD51 Series',
        'price': 6995,
        'in_stock': 100,
    },
    'Panasonic_9': {
        'title': 'Panasonic KX-TGE474S',
        'category': 'Panasonic',
        'img_url': 'https://shop.panasonic.com/dw/image/v2/AASQ_PRD/on/demandware.static/-/Sites-shop-pna-master-catalog/default/dwa5e8a258/product/images/KX-TGEA40S_ALT01.jpg?sw=1000&sh=1000&sm=fit',
        'article': 'KX-TGE474S',
        'description': 'Link2Cell Bluetooth® Cordless Phone with Large Keypad- KX-TGE47 Series',
        'price': 14995,
        'in_stock': 100,
    },
    'Panasonic_10': {
        'title': 'Panasonic KX-TGM450S',
        'category': 'Panasonic',
        'img_url': 'https://shop.panasonic.com/dw/image/v2/AASQ_PRD/on/demandware.static/-/Sites-shop-pna-master-catalog/default/dw10b42aa1/product/images/KX-TGM450S_ALT01.jpg?sw=1000&sh=1000&sm=fit',
        'article': 'KX-TGM450S',
        'description': 'Amplified Cordless Phone with Digital Answering Machine - 1 Handset - KX-TGM450S',
        'price': 15995,
        'in_stock': 100,
    },
    ### VTech ###
    'VTech_1': {
        'title': 'VTech DS662V-1H',
        'category': 'VTech',
        'img_url': 'https://cdn-web.vtp-media.com/products/DS/DS662V-X/DS662V-1H-Connect-to-Cell-Phone-System-with-Caller-ID-Call-Waiting-Straight-min.jpg',
        'article': 'DS662V-1H',
        'description': '5 Handset Connect to Cell™ Phone System with Caller ID/Call Waiting',
        'price': 14975,
        'in_stock': 0,
    },
    'VTech_2': {
        'title': 'VTech DS662V-1G',
        'category': 'VTech',
        'img_url': 'https://cdn-web.vtp-media.com/products/DS/DS662V-X/DS662V-1G+twoDS660V-1F+twoDS660V-1J_5_Handset_Connect_to_Cell_Phone_System_with_Caller-min.jpg',
        'article': 'DS662V-1G',
        'description': '4 Handset Connect to Cell™ Phone System with Caller ID/Call Waiting',
        'price': 9495,
        'in_stock': 100,
    },
    'VTech_3': {
        'title': 'VTech ST_6421',
        'category': 'VTech',
        'img_url': 'https://cdn-web.vtp-media.com/products/TR/TRX-2013/TR16-2013+oneTR02-2013+twoTR07-2013+oneTR06-2013_5-Handset-FoneDeco-Answering-System-with-Caller-ID-Call-Waiting-min.jpg',
        'article': 'ST_6421',
        'description': '7 Handset Connect to Cell™ Answering System with Caller ID/Call Waiting',
        'price': 18495,
        'in_stock': 100,
    },
    ### Samsung ###
    'Samsung_1': {
        'title': 'Samsung Galaxy M30s 4/64GB Black',
        'category': 'Samsung',
        'img_url': 'https://i2.rozetka.ua/goods/14073152/samsung_galaxy_m30s_4_64gb_black_images_14073152845.jpg',
        'article': 'samsung_galaxy_m30s_4_64gb_black',
        'description': 'Экран (6.4", Super AMOLED, 2340х1080) / Samsung Exynos 9611 (4 x 2.3 ГГц + 4 x 1.7 ГГц) / тройная основная камера: 48 Мп + 8 Мп + 5 Мп, фронтальная 16 Мп / RAM 4 ГБ / 64 ГБ встроенной памяти + microSD (до 512 ГБ) / 3G / LTE / GPS / ГЛОНАСС / BDS / Galileo / поддержка 2х SIM-карт (Nano-SIM) / Android 9.0 (Pie) / 6000 мА*ч',
        'price': 599900,
        'in_stock': 100,
    },
    'Samsung_2': {
        'title': 'Samsung Galaxy S9 4/64GB Black',
        'category': 'Samsung',
        'img_url': 'https://i1.rozetka.ua/goods/3249371/samsung_galaxy_s9_64gb_black_images_3249371727.jpg',
        'article': 'samsung_galaxy_s9_64gb_black',
        'description': 'Экран (5.8", Super AMOLED, 2960х1440)/ Samsung Exynos 9810 (4 x 2.7 ГГц + 4 x 1.7 ГГц)/ основная камера 12 Мп + фронтальная 8 Мп/ RAM 4 ГБ/ 64 ГБ встроенной памяти + microSD (до 400 ГБ)/ 3G/ LTE/ GPS/ поддержка 2х SIM-карт (Nano-SIM)/ Android 8.0 (Oreo) / 3000 мА*ч',
        'price': 1099900,
        'in_stock': 100,
    },
    'Samsung_3': {
        'title': 'Samsung Galaxy A51 6/128GB White',
        'category': 'Samsung',
        'img_url': 'https://i8.rozetka.ua/goods/16041151/copy_samsung_sm_a515fzwusek_5e04c47d16006_images_16041151799.jpg',
        'article': 'copy_samsung_sm_a515fzwusek',
        'description': 'Экран (5.8", Super AMOLED, 2960х1440)/ Samsung Exynos 9810 (4 x 2.7 ГГц + 4 x 1.7 ГГц)/ основная камера 12 Мп + фронтальная 8 Мп/ RAM 4 ГБ/ 64 ГБ встроенной памяти + microSD (до 400 ГБ)/ 3G/ LTE/ GPS/ поддержка 2х SIM-карт (Nano-SIM)/ Android 8.0 (Oreo) / 3000 мА*ч',
        'price': 949900,
        'in_stock': 10000,
    },
    'Xiaomi_1': {
        'title': 'Xiaomi Redmi 7A 2/16GB Matte Black',
        'category': 'Xiaomi',
        'img_url': 'https://i1.rozetka.ua/goods/12939803/xiaomi_redmi_7a_2_16gb_matte_black_eu_images_12939803028.jpg',
        'article': 'xiaomi_redmi_7a_2_16gb_matte_black',
        'description': 'Экран (5.45'', IPS, 1440x720)/ Qualcomm Snapdragon 439 (4 x 1.95 ГГц + 4 х 1.45 ГГц)/ основная камера: 13 Мп, фронтальная камера: 5 Мп/ RAM 2 ГБ/ 16 ГБ встроенной памяти + microSD (до 256 ГБ)/ 3G/ LTE/ GPS/ ГЛОНАСС/ поддержка 2х SIM-карт (Nano-SIM)/ Android 9.0 (Pie)/ 4000 мА*ч',
        'price': 219900,
        'in_stock': 0,
    },
    'Xiaomi_2': {
        'title': 'Xiaomi Redmi Note 8T 4/64GB Starscape Blue',
        'category': 'Xiaomi',
        'img_url': 'https://i1.rozetka.ua/goods/14838562/copy_xiaomi_redmi_note_8_4_64gb_blue_5dbc4a4d6606e_images_14838562202.jpg',
        'article': 'copy_xiaomi_redmi_note_8t_524153',
        'description': 'Экран (6.3", IPS, 2340x1080)/ Qualcomm Snapdragon 665 (2.0 ГГц)/ квадро основная камера: 48 Мп + 8 Мп + 2 Мп + 2 Мп, фронтальная камера: 13 Мп/ RAM 4 ГБ/ 64 ГБ встроенной памяти + microSD (до 256 ГБ)/ 3G/ LTE/ GPS/ поддержка 2х SIM-карт (Nano-SIM)/ Android 9.0 (Pie) / 4000 мА*ч',
        'price': 499900,
        'in_stock': 18,
    },
    'Xiaomi_3': {
        'title': 'Xiaomi Redmi Note 8 Pro 6/64GB Blue',
        'category': 'Xiaomi',
        'img_url': 'https://i8.rozetka.ua/goods/16255384/xiaomi_redmi_note_8_pro_664gb_green_images_16255384622.jpg',
        'article': 'xiaomi_redmi_note_8_pro_6_64gb_blue',
        'description': 'Экран (6.53", IPS, 2340x1080)/ MediaTek Helio G90T (2 x 2.05 ГГц + 6 x 2.0 ГГц)/ квадро основная камера: 64 Мп + 8 Мп + 2 Мп + 2 Мп, фронтальная камера: 20 Мп/ RAM 6 ГБ/ 64 ГБ встроенной памяти + microSD (до 256 ГБ)/ 3G/ LTE/ GPS/ поддержка 2х SIM-карт (Nano-SIM)/ Android 9.0 (Pie) / 4500 мА*ч',
        'price': 599900,
        'in_stock': 11,
    },
    'Intel_1': {
        'title': 'Intel Core i5-9400F 2.9GHz/8GT/s/9MB',
        'category': 'Intel',
        'img_url': 'https://i1.rozetka.ua/goods/10930275/intel_core_i5_9400f_bx80684i59400f_images_10930275105.jpg',
        'article': 'intel_core_i5_9400f',
        'description': 'Процессор Intel Core i5-9400F 2.9GHz/8GT/s/9MB (BX80684I59400F) s1151 BOX',
        'price': 455000,
        'in_stock': 1,
    },
    'Intel_2': {
        'title': 'Intel Core i3-8100 3.6GHz/8GT/s/6MB',
        'category': 'Intel',
        'img_url': 'https://i2.rozetka.ua/goods/2238131/intel_core_i3_8100_images_2238131224.jpg',
        'article': 'intel_core_i3_8100',
        'description': 'Процессор Intel Core i3-8100 3.6GHz/8GT/s/6MB (BX80684I38100) s1151 BOX',
        'price': 355500,
        'in_stock': 3,
    },
    'Intel_3': {
        'title': 'Intel Core i9-9900K 3.6GHz/8GT/s/16MB',
        'category': 'Intel',
        'img_url': 'https://i2.rozetka.ua/goods/10531195/copy_intel_core_i9_9900k_bx80684i99900k_5c4b32fdea299_images_10531195292.jpg',
        'article': 'intel_core_i9_9900k',
        'description': 'Процессор Intel Core i9-9900K 3.6GHz/8GT/s/16MB (BX80684I99900K) s1151 BOX',
        'price': 1572000,
        'in_stock': 3,
    },
    'AMD_1': {
        'title': 'AMD Ryzen 5 3600 3.6GHz/32MB',
        'category': 'AMD',
        'img_url': 'https://i1.rozetka.ua/goods/12765145/amd_ryzen_5_3600_images_12765145099.jpg',
        'article': 'amd_ryzen_5_3600',
        'description': 'Процессор AMD Ryzen 5 3600 3.6GHz/32MB (100-100000031BOX) sAM4 BOX',
        'price': 543000,
        'in_stock': 3,
    },
    'AMD_2': {
        'title': 'AMD Ryzen 5 1600 3.2GHz/16MB',
        'img_url': 'https://i2.rozetka.ua/goods/13656299/amd_ryzen_5_1600_wraith_stealth_images_13656299167.jpg',
        'category': 'AMD',
        'article': 'amd_ryzen_5_1600_wraith_stealth',
        'description': 'Процессор AMD Ryzen 5 1600 3.2GHz/16MB (YD1600BBAFBOX) sAM4 BOX',
        'price': 290000,
        'discount_price': 250000,
        'in_stock': 0,
    },
    'AMD_3': {
        'title': 'AMD Ryzen Threadripper 2990WX 3.0GHz/64MB',
        'img_url': 'https://i1.rozetka.ua/goods/7348932/amd_ryzen_threadripper_2990wx_images_7348932162.jpg',
        'category': 'AMD',
        'article': 'amd_ryzen_threadripper_2990wx',
        'description': 'Процессор AMD Ryzen Threadripper 2990WX 3.0GHz/64MB (YD299XAZAFWOF) sTR4 BOX',
        'price': 4900000,
        'discount_price': 4500000,
        'in_stock': 1,
    },
}


class ShopDataGenerator:

    @staticmethod
    def generate_data():
        Category.drop_collection()
        Cart.drop_collection()
        CartProduct.drop_collection()
        Product.drop_collection()

        recursive_categories_creation(categories_json)

        cat_id_dict = {}
        [cat_id_dict.update({cat_name: get_cat_id(cat_name)}) for cat_name in categories_description_dict]

        for product in products_dict.values():
            product['category'] = cat_id_dict[product['category']]
            Product.objects.create(**product)


def recursive_categories_creation(cat_json, previous_cat=None, level=0):
    for key, value in cat_json.items():

        root_category_dict = {
            'title': key,
            'description': categories_description_dict[key],
            'is_root': True if level == 0 else False
        }

        category = Category.create(**root_category_dict)
        if previous_cat:
            previous_cat.add_subcategory(category)

        if value:
            recursive_categories_creation(cat_json[key], category, level=level + 1)


if __name__ == '__main__':
    ShopDataGenerator.generate_data()
