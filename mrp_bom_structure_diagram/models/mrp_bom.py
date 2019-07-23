# Copyright 2019 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class MrpBom(models.Model):
    """ Defines bills of material for a product or a product template """
    _inherit = 'mrp.bom'

    def _get_bom_vals(self, part_id, parent, bom_qty):
        return {
            'id': part_id,
            'pid': parent,
            'description': "%s x " % bom_qty,
            'name': self.product_tmpl_id.display_name,
            'db_id': self.product_tmpl_id.id,
        }

    @api.model
    def _get_line_vals(self, line, part_id, parent, line_qty):
        return {
            'id': part_id,
            'pid': parent,
            'description': "%s x " % line_qty,
            'name': (line.product_id.display_name or
                     line.product_tmpl_id.display_name),
            'db_id': line.product_tmpl_id.id,
        }

    @api.multi
    def get_bom_data(self, result=None, qty_factor=1, part_id=1, parent=0):
        """Returns data formatted for diagram
        """
        self.ensure_one()
        if result is None:
            result = []
        qty_factor = self.product_qty / qty_factor
        bom_qty = self.product_qty / qty_factor
        result.append(self._get_bom_vals(part_id, parent, bom_qty))
        parent += 1
        part_id += 1
        for line in self.bom_line_ids:
            sub_bom = self._bom_find(product=line.product_id)
            if sub_bom:
                result, part_id = sub_bom.get_bom_data(
                    result, 1/qty_factor, part_id, parent)
            else:
                line_qty = line.product_qty / qty_factor
                result.append(
                    self._get_line_vals(line, part_id, parent, line_qty))
                part_id += 1
        return result, part_id
