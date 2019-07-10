# Copyright 2019 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class MrpBom(models.Model):
    """ Defines bills of material for a product or a product template """
    _inherit = 'mrp.bom'

    @api.multi
    def get_bom_data(self, result=None, part_id=1, parent=0):
        """Returns data formatted for diagram
        """
        self.ensure_one()
        if result is None:
            result = []
        result.append({
            'id': part_id,
            'pid': parent,
            'name': self.product_tmpl_id.display_name,
            'db_id': self.product_tmpl_id.id,
        })
        parent += 1
        part_id += 1
        for line in self.bom_line_ids:
            sub_bom = self._bom_find(product=line.product_id)
            if sub_bom:
                result, part_id = sub_bom.get_bom_data(result, part_id, parent)
            else:
                result.append({
                    'id': part_id,
                    'pid': parent,
                    'name': (line.product_id.display_name or
                             line.product_tmpl_id.display_name),
                    'db_id': line.product_tmpl_id.id,
                })
                part_id += 1
        return result, part_id
