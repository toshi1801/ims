# vendor info
vendor_query_1 ="select v.vendor_id as vendor_id, v.address_id as address_id, ad.street as vendor_street, " \
                " ad.city as vendor_city, ad.state as vendor_state," \
                "ad.zip_code as vendor_zipcode, v.vendor_name, v.mobile, v.email " \
                "from address ad, vendor v where ad.address_id=v.address_id and " \
                "v.vendor_id='{}'"

# vendor product info
vendor_query_2 ="select p.product_id, p.product_name, vp.price, p.brand, p.category, vp.quantity from vendor v, " \
                "vendor_product vp ,product p where v.vendor_id = vp.vendor_id and vp.product_id = p.product_id " \
                "and v.vendor_id = '{}' group by p.product_id, p.product_name, vp.price, p.brand, p.category, vp.quantity; "\

# vendor payment info
vendor_query_3 ="select p.type as type, account_name, account_number, routing_number, paypal_id, venmo_id " \
                "from vendor v, payment p where v.payment_id = p.payment_id and v.vendor_id='{}'; "\

# vendor product search
vendor_query_4 ="select p.product_name, vp.quantity, vp.price, p.brand, p.category from  vendor_product vp, product p "\
                "where p.product_name = '{}' and p.product_id = vp.product_id and vp.vendor_id = '{}' " \

vendor_query_5 ="insert into vendor_product (vendor_product_id, product_id, vendor_id, quantity, date_added,"\
                "price) VALUES ('{vendor_product_id}','{product_id}','{vendor_id}','{quantity}','{date_added}','{price}')"\

# vendor order history
vendor_query_6 = "select v.vendor_id, v.vendor_name, po.invoice_id, po.product_id, po.price as total_cost, " \
                "po.quantity, po.date_placed, p.product_name, p.brand, p.category, p.product_info, " \
                "(po.price/po.quantity) as price, po.payment_status from vendor v, orders po, product p " \
                "where v.vendor_id=po.vendor_id and po.product_id=p.product_id and v.vendor_id='{}'"

vendor_query_8 = "select v.vendor_id, v.vendor_name, po.admin_id, po.invoice_id, po.product_id, po.price as total_cost, " \
                "po.quantity, po.date_placed, p.product_name, p.brand, p.category, p.product_info, " \
                "(po.price/po.quantity) as price, po.payment_status from vendor v, orders po, product p " \
                "where v.vendor_id=po.vendor_id and po.product_id=p.product_id and v.vendor_id='{}' and invoice_id='{}'"

vendor_query_9 = "select w.warehouse_id, w.name, a.address_id, a.street, a.city, a.state, a.zip_code from warehouse w, " \
                "address a where w.address_id=a.address_id and admin_id='{}'"

vendor_query_10 = "select v.vendor_id, v.vendor_name, a.address_id, a.street, a.city, a.state, a.zip_code from " \
                 "vendor v, address a where v.address_id=a.address_id and vendor_id='{}'"

vendor_query_11 = "select product_id from product where brand='{brand}' and category='{category}' "\
                  "and product_name = '{product_name}';"

vendor_query_12 = "update vendor_product set quantity='{quantity}' where vendor_id='{vendor_id}' and product_id='{product_id}';"

vendor_query_13 = "delete from vendor_product where product_id='{product_id}' and vendor_id='{vendor_id}';"
