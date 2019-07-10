# Copyright 2019 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Mrp Bom Structure Diagram',
    'summary': """
        MRP BoM Structure diagram""",
    'version': '12.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Eficent Business and IT Consulting Services S.L.,'
              'Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/manufacture-reporting',
    'depends': ['mrp'],
    'data': [
        'views/mrp_templates.xml',
    ],
    'qweb': ['static/src/xml/mrp.xml'],
    'installable': True,
}
