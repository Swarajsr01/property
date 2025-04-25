/** @odoo-module */
import { renderToElement } from "@web/core/utils/render";
import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";
function chunkArray(array, size) {
    const chunks = [];
    for (let i = 0; i < array.length; i += size) {
        chunks.push(array.slice(i, i + size));
    }
    return chunks;
}

publicWidget.registry.get_product_tab = publicWidget.Widget.extend({
    selector : '.categories_section',
    async willStart() {
        const result = await rpc('/get_properties_categories', {});
        if(result && result.properties){
//            let fragment = renderToFragment('property.category_data', { result: result });
              const chunks = chunkArray(result.properties, 4);
//            this.$target.empty().append(fragment);
              this.$target.empty().html(renderToElement('property.category_data', {chunks: chunks}))
        }
    },
});
