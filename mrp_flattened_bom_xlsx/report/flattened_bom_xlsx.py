# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging
from odoo.report import report_sxw
from odoo.tools.translate import _
from odoo.addons.mrp_bom_structure_xlsx.report.bom_structure_xlsx import \
    BomStructureXlsx

_logger = logging.getLogger(__name__)

try:
    from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx
except ImportError:
    _logger.debug("report_xlsx not installed, Excel export non functional")

    class ReportXlsx(object):
        def __init__(self, *args, **kwargs):
            pass


class FlattenedBomXlsx(BomStructureXlsx):

    def print_flattened_bom_lines(self, bom, requirements, sheet, row):
        i = row
        sheet.write(i, 0, bom.product_tmpl_id.name or '')
        sheet.write(i, 1, bom.code or '')
        sheet.write(i, 2, bom.display_name or '')
        sheet.write(i, 3, bom.product_qty)
        sheet.write(i, 4, bom.product_uom_id.name or '')
        sheet.write(i, 5, bom.code or '')
        i += 1
        for product, total_qty in requirements.iteritems():
            sheet.write(i, 1, product.default_code or '')
            sheet.write(i, 2, product.display_name or '')
            sheet.write(i, 3, total_qty or 0.0)
            sheet.write(i, 4, product.uom_id.name or '')
            sheet.write(i, 5, product.code or '')
            i += 1
        return i

    def generate_xlsx_report(self, workbook, data, objects):

        def _compute_flattened_totals(bom, factor=1):
            factor *= bom.product_qty
            for line in bom.bom_line_ids:
                sub_bom = bom._bom_find(product=line.product_id)
                if sub_bom:
                    _compute_flattened_totals(sub_bom, factor)
                else:
                    if totals.get(line.product_id):
                        totals[line.product_id] += line.product_uom_id.\
                            _compute_quantity(
                            line.product_qty*factor, line.product_id.uom_id)
                    else:
                        totals[line.product_id] = line.product_uom_id.\
                            _compute_quantity(
                            line.product_qty*factor, line.product_id.uom_id)

        workbook.set_properties({
            'comments': 'Created with Python and XlsxWriter from Odoo 9.0'})
        sheet = workbook.add_worksheet(_('Flattened BOM'))
        sheet.set_landscape()
        sheet.fit_to_pages(1, 0)
        sheet.set_zoom(80)
        sheet.set_column(0, 0, 40)
        sheet.set_column(1, 2, 20)
        sheet.set_column(3, 3, 40)
        sheet.set_column(4, 6, 20)
        title_style = workbook.add_format({'bold': True,
                                           'bg_color': '#FFFFCC',
                                           'bottom': 1})
        sheet_title = [_('BOM Name'),
                       _('Product Reference'),
                       _('Product Name'),
                       _('Quantity'),
                       _('Unit of Measure'),
                       _('Reference')
                       ]
        sheet.set_row(0, None, None, {'collapsed': 1})
        sheet.write_row(1, 0, sheet_title, title_style)
        sheet.freeze_panes(2, 0)
        i = 2
        for o in objects:
            totals = {}
            _compute_flattened_totals(o)
            i = self.print_flattened_bom_lines(o, totals, sheet, i)


FlattenedBomXlsx('report.flattened.bom.xlsx', 'mrp.bom',
                 parser=report_sxw.rml_parse)
