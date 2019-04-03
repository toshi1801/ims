admin_query_1 = "select p.product_id, p.product_name, count(*) from warehouse as w, warehouse_product as wp, " \
                "product as p where admin_id='{}' and wp.warehouse_id=w.warehouse_id and p.product_id=wp.product_id " \
                "group by (p.product_id, p.product_name)"

admin_query_2 = "select * from admin where admin_id='{}'"

admin_query_3 = "SELECT budget, budget-(SELECT SUM(price) FROM placed_order WHERE admin_id='{id}' AND " \
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
                "(po.price/po.quantity) as price from vendor v, placed_order po, product p " \
                "where v.vendor_id=po.vendor_id and po.product_id=p.product_id and admin_id='{}'"
