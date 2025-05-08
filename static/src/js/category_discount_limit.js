/** @odoo-module **/

console.log("test")
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { patch } from "@web/core/utils/patch";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { _t } from "@web/core/l10n/translation";
import { rpc } from "@web/core/network/rpc";


patch(PaymentScreen.prototype, {
    setup() {
        super.setup();
        this.pos = usePos();
//        this.fetchConfigValues();
    },


    async validateOrder(isForceValidate) {
        const session = this.pos.config.current_session_id;
        const order = this.pos.get_order();
//        const maxAllowedDiscount = session?.max_discount ?? 0;
//        console.log(maxAllowedDiscount)
        let totalCategoryDiscount = 0;
        const result = await rpc("/pos/get_category_settings_discount", {});
//        console.log(result)

        const currentOrder = this.pos.get_order();
        for (const line of currentOrder.get_orderlines()) {
            const product = line.get_product();
            product.pos_categ_ids.forEach(cat => {
                if (result.category_ids.includes(cat.id)) {
                    const unitPrice = line.get_unit_price();
                    const discount = line.get_discount();
                    const quantity = line.get_quantity();
                    const lineDiscountAmount = (unitPrice * discount / 100) * quantity;
//                    console.log(product.discount)
//                    console.log(unitPrice)
                    console.log(discount)
//                    console.log(quantity)
//                    console.log(lineDiscountAmount)
                    totalCategoryDiscount += lineDiscountAmount
                }
                else{
                    console.log("this category not added to the settings")
                }
            });
        }
        console.log(totalCategoryDiscount)
//        console.log(config.selected_category_ids)
//        console.log(category_discount_limit)
//        console.log(category_discount_category_ids)
//        console.log(order)
//        const session_discount_limit_amount = session?.session_discount_limit_amount ?? 0;

//        if (session_discount_limit) {
//
//            let totalLineDiscount = 0;
//            let totalGlobalDiscount = 0;
//            const discountProductId = this.pos.config.discount_product_id?.id;
//
//            order.get_orderlines().forEach(line => {
//                if (line.product_id?.id === discountProductId) {
//                    totalGlobalDiscount += Math.abs(line.get_price_with_tax());
//                } else {
//                    const unitPrice = line.get_unit_price();
//                    const discount = line.get_discount();
//                    const quantity = line.get_quantity();
//
//                    totalLineDiscount += (unitPrice * discount / 100) * quantity;
//                }
//            });
//
//            const totalDiscount = totalLineDiscount + totalGlobalDiscount;
//
//            if (totalDiscount > session_discount_limit_amount || session_discount_limit_amount <= 0) {
//                await this.notification.add(_t("Session discount limit exceeded."), {
//                    title: "Validation Error",
//                    type: "warning"
//                });
//                return;
//            }
//            await rpc("/pos/update_session_discount_limit", {
//                session_id: session.id,
//                used_discount: totalDiscount
//            });
//        }
        return super.validateOrder(isForceValidate);
    }
});

