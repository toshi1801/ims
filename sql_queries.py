admin_query_1 = "select p.product_id, p.product_name, p.brand, p.category, count(*) from warehouse as w, " \
                "warehouse_product as wp, product as p where admin_id='{}' and wp.warehouse_id=w.warehouse_id and " \
                "p.product_id=wp.product_id group by p.product_id, p.product_name, p.brand, p.category"

admin_query_2 = "select * from admin where admin_id='{}'"

admin_query_3 = "SELECT budget, budget-(SELECT SUM(price) FROM orders WHERE admin_id='{id}' AND " \
                "date_placed > date_trunc('month', current_date) GROUP BY admin_id) as remaining_balance " \
                "FROM admin WHERE admin_id='{id}'"

admin_query_4 = "select vp.vendor_id, v.vendor_name, vp.vendor_product_id, vp.product_id, p.product_name, p.brand, " \
                "p.category, vp.quantity, vp.price from vendor v, vendor_product vp, product p " \
                "where v.vendor_id=vp.vendor_id and vp.product_id=p.product_id;"

admin_query_5 = "select ad1.street as admin_street, ad1.city as admin_city, ad1.state as admin_state, " \
                "ad1.zip_code as admin_zipcode, a.admin_name, a.mobile, a.email, a.dob, w.name as warehouse_name, " \
                "ad2.street as w_street, ad2.city as w_city, ad2.state as w_state, ad2.zip_code as w_zipcode " \
                "from address ad1, admin a, warehouse w, address ad2 where ad1.address_id=a.address_id and " \
                "a.warehouse_id=w.warehouse_id and w.address_id=ad2.address_id and a.admin_id='{}'"

admin_query_6 = "select v.vendor_id, v.vendor_name, po.invoice_id, po.product_id, po.price as total_cost, " \
                "po.quantity, po.date_placed, p.product_name, p.brand, p.category, p.product_info, " \
                "(po.price/po.quantity) as price, po.payment_status from vendor v, orders po, product p " \
                "where v.vendor_id=po.vendor_id and po.product_id=p.product_id and admin_id='{}'"

admin_query_7 = "select * from product where product_id='{}'"

admin_query_8 = "select v.vendor_id, v.vendor_name, po.invoice_id, po.product_id, po.price as total_cost, " \
                "po.quantity, po.date_placed, p.product_name, p.brand, p.category, p.product_info, " \
                "(po.price/po.quantity) as price, po.payment_status from vendor v, orders po, product p " \
                "where v.vendor_id=po.vendor_id and po.product_id=p.product_id and admin_id='{}' and invoice_id='{}'"

admin_query_9 = "select w.warehouse_id, w.name, a.address_id, a.street, a.city, a.state, a.zip_code from warehouse w, " \
                "address a where w.address_id=a.address_id and admin_id='{}'"

admin_query_10 = "select v.vendor_id, v.vendor_name, a.address_id, a.street, a.city, a.state, a.zip_code from " \
                 "vendor v, address a where v.address_id=a.address_id and vendor_id='{}'"

admin_query_11 = "select distinct(brand) from product where category='{}'"

admin_query_12 = "select distinct(product_name) from product where category='{}' and brand='{}'"

admin_query_13 = "select p.product_id, p.product_name, vp.vendor_product_id, v.vendor_id, v.vendor_name, " \
                 "vp.quantity, vp.price from product p, vendor_product vp, vendor v where p.product_id=vp.product_id" \
                 " and vp.vendor_id=v.vendor_id and p.category='{}' and p.brand='{}' and " \
                 "p.product_name='{}'"

admin_query_14 = "select warehouse_id from warehouse where admin_id='{}'"

admin_query_15 = "insert into orders (invoice_id, admin_id, vendor_id, warehouse_id, product_id, payment_status, " \
                 "price, quantity, date_placed) VALUES ('{invoice_id}', '{admin_id}', '{vendor_id}', " \
                 "'{warehouse_id}', '{product_id}', '{payment_status}', {price}, {quantity}, '{date_placed}')"

admin_query_16 = "update vendor_product set quantity=quantity-{} where vendor_product_id='{}'"
