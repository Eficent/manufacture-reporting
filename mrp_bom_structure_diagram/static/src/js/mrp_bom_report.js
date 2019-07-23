odoo.define('mrp.mrp_bom_report_diagram', function (require) {
    'use strict';

    var core = require('web.core');
    var framework = require('web.framework');
    var MrpBomReport = require('mrp.mrp_bom_report');

    var QWeb = core.qweb;
    var _t = core._t;

    MrpBomReport.include({
        renderSearch: function () {
            this._super()
            this.$buttonPrint.filter('.o_mrp_bom_show_diagram').on('click', this._onClickDiagram.bind(this));
        },
        _onClickDiagram: function (ev) {
            var should_render = this._toggleButton()
            if (should_render) {
                var self = this;
                var activeID = this.given_context.active_id;
                return this._rpc({
                    model: 'mrp.bom',
                    method: 'get_bom_data',
                    args: [activeID,]
                })
                .then(function (bom_data) {
                    self._renderDiagram(bom_data[0]);
                });
            }
        },
        _renderDiagram: function (bom_data) {
            var self = this;
            $(".o_mrp_bom_report_page").after(function() {
                return '<div id="diagram" class="container o_mrp_bom_report_page">' +
                        '<div class="row"><div class="col-lg-12"><h1>BoM Diagram</h1></div></div>' +
                        '<div style="width:100%; margin:20px;" id="orgchart" class="orgchart"/>' +
                       '</div>';
            });

            OrgChart.templates.myTemplate = Object.assign({}, OrgChart.templates.ana);
//            OrgChart.templates.myTemplate.size = [100, 100];
//            OrgChart.templates.myTemplate.node = '<circle cx="50" cy="50" r="50" fill="#4D4D4D" stroke-width="1" stroke="#1C1C1C"></circle>';
//            OrgChart.templates.myTemplate.ripple = {
//                radius: 50,
//                color: "#0890D3",
//                rect: null
//            };
            OrgChart.templates.myTemplate.field_0 = '<text width="230" text-overflow="multiline" style="font-size: 16px;font-weight: bold;" fill="#ffffff" x="125" y="90" text-anchor="middle">{val}</text>';
            OrgChart.templates.myTemplate.field_1 = '<text width="230" style="font-size: 20px;border: 5px solid #00bfb6;" fill="#ffffff" x="125" y="60" text-anchor="middle">{val}</text>';

            var chart = new OrgChart(document.getElementById("orgchart"), {
                template: "myTemplate",
                showXScroll: BALKANGraph.scroll.visible,
                showYScroll: BALKANGraph.scroll.visible,
                mouseScrool: BALKANGraph.action.yScroll,
                enableSearch: false,
                nodeBinding: {
                    field_0: "name",
                    field_1: "description",
                    img_0: "img"
                },
                scaleInitial: OrgChart.match.width,
                nodes: bom_data,
                onClick: function (sender, node) {
                    var action = {
                        type:'ir.actions.act_window',
                        view_type: 'form',
                        view_mode: 'form',
                        res_model: 'product.template',
                        views: [[false, 'form']],
                        target: 'current',
                        res_id: node['db_id'],
                    };
                    self.do_action(action);
                    return false
                },
            });
        },
        _toggleButton: function () {
            if ($('#showDiagram').text() == 'show diagram') {
                $(".o_mrp_bom_report_page").css("display", "none");
                $('#showDiagram').text('hide diagram')
                return true
            } else {
                $('#showDiagram').text('show diagram')
                $(".o_mrp_bom_report_page").css("display", "block");
                $('#diagram').remove()
                return false
            }
        },
    });

    return MrpBomReport;

});