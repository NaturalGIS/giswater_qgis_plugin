"""
This file is part of Giswater 2.0
The program is free software: you can redistribute it and/or modify it under the terms of the GNU
General Public License as published by the Free Software Foundation, either version 3 of the License,
or (at your option) any later version.
"""

# -*- coding: utf-8 -*-
from PyQt4.Qt import QDate, QDateTime
from PyQt4.QtCore import QPoint, Qt, QObject, SIGNAL
from PyQt4.QtGui import QCompleter, QStringListModel, QDateEdit, QLineEdit, QTabWidget, QTableView, QColor, QStringListModel, QCompleter, QDateTimeEdit, QPushButton, QCheckBox, QComboBox
from qgis.core import QgsMapLayerRegistry, QgsFeatureRequest, QgsExpression, QgsPoint           # @UnresolvedImport
from qgis.gui import QgsMapToolEmitPoint, QgsMapCanvasSnapper, QgsMapTool, QgsRubberBand, QgsVertexMarker
from PyQt4.QtSql import QSqlTableModel

import os
import sys
from datetime import datetime
from functools import partial

plugin_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(plugin_path)
import utils_giswater

from ui.change_node_type import ChangeNodeType    # @UnresolvedImport
from ui.add_doc import AddDoc                     # @UnresolvedImport
from ui.event_standard import EventStandard                     # @UnresolvedImport
from ui.event_ud_arc_standard import EventUDarcStandard                     # @UnresolvedImport
from ui.event_ud_arc_rehabit import EventUDarcRehabit                     # @UnresolvedImport
from ui.add_element import AddElement             # @UnresolvedImport
from ui.add_visit import AddVisit             # @UnresolvedImport
from ui.config_edit import ConfigEdit             # @UnresolvedImport
from ui.topology_tools import TopologyTools       # @UnresolvedImport
from multiple_snapping import MultipleSnapping                  # @UnresolvedImport
from ui.ud_catalog import UDcatalog               # @UnresolvedImport
from ui.ws_catalog import WScatalog               # @UnresolvedImport



from parent import ParentAction


class Edit(ParentAction):

    def __init__(self, iface, settings, controller, plugin_dir):
        """ Class to control toolbar 'edit' """
        
        self.minor_version = "3.0"
        ParentAction.__init__(self, iface, settings, controller, plugin_dir)
        # Get tables or views specified in 'db' config section

        self.iface = iface
        self.settings = settings
        self.controller = controller
        self.plugin_dir = plugin_dir
        self.canvas = self.iface.mapCanvas()

        self.table_arc = self.settings.value('db/table_arc', 'v_edit_arc')
        self.table_node = self.settings.value('db/table_node', 'v_edit_node')
        self.table_connec = self.settings.value('db/table_connec', 'v_edit_connec')
        self.table_gully = self.settings.value('db/table_gully', 'v_edit_gully')

        self.table_man_arc = self.settings.value('db/table_man_arc', 'v_edit_man_arc')
        self.table_man_node = self.settings.value('db/table_man_node', 'v_edit_man_node')
        self.table_man_connec = self.settings.value('db/table_man_connec', 'v_edit_man_connec')
        self.table_man_gully = self.settings.value('db/table_man_gully', 'v_edit_man_gully')

        self.table_version = self.settings.value('db/table_version', 'version')

        # Tables connec_group
        self.table_wjoin = self.settings.value('db/table_wjoin', 'v_edit_man_wjoin')
        self.table_tap = self.settings.value('db/table_tap', 'v_edit_man_tap')
        self.table_greentap = self.settings.value('db/table_greentap', 'v_edit_man_greentap')
        self.table_fountain = self.settings.value('db/table_fountain', 'v_edit_man_fountain')

        # Tables node_group
        self.table_tank = self.settings.value('db/table_tank', 'v_edit_man_tank')
        self.table_pump = self.settings.value('db/table_pump', 'v_edit_man_pump')
        self.table_source = self.settings.value('db/table_source', 'v_edit_man_source')
        self.table_meter = self.settings.value('db/table_meter', 'v_edit_man_meter')
        self.table_junction = self.settings.value('db/table_junction', 'v_edit_man_junction')
        self.table_waterwell = self.settings.value('db/table_waterwell', 'v_edit_man_waterwell')
        self.table_reduction = self.settings.value('db/table_reduction', 'v_edit_man_reduction')
        self.table_hydrant = self.settings.value('db/table_hydrant', 'v_edit_man_hydrant')
        self.table_valve = self.settings.value('db/table_valve', 'v_edit_man_valve')
        self.table_manhole = self.settings.value('db/table_manhole', 'v_edit_man_manhole')

        # Tables arc_group
        self.table_varc = self.settings.value('db/table_varc', 'v_edit_man_varc')
        self.table_siphon = self.settings.value('db/table_siphon', 'v_edit_man_siphon')
        self.table_conduit = self.settings.value('db/table_conduit', 'v_edit_man_conduit')
        self.table_waccel = self.settings.value('db/table_waccel', 'v_edit_man_waccel')

        self.table_chamber = self.settings.value('db/table_chamber', 'v_edit_man_chamber')
        self.table_chamber_pol = self.settings.value('db/table_chamber', 'v_edit_man_chamber_pol')
        self.table_netgully = self.settings.value('db/table_netgully', 'v_edit_man_netgully')
        self.table_netgully_pol = self.settings.value('db/table_netgully_pol', 'v_edit_man_netgully_pol')
        self.table_netinit = self.settings.value('db/table_netinit', 'v_edit_man_netinit')
        self.table_wjump = self.settings.value('db/table_wjump', 'v_edit_man_wjump')
        self.table_wwtp = self.settings.value('db/table_wwtp', 'v_edit_man_wwtp')
        self.table_wwtp_pol = self.settings.value('db/table_wwtp_pol', 'v_edit_man_wwtp_pol')
        self.table_storage = self.settings.value('db/table_storage', 'v_edit_man_storage')
        self.table_storage_pol = self.settings.value('db/table_storage_pol', 'v_edit_man_storage_pol')
        self.table_outfall = self.settings.value('db/table_outfall', 'v_edit_man_outfall')

        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        self.snapper = QgsMapCanvasSnapper(self.canvas)

        # Vertex marker
        self.vertex_marker = QgsVertexMarker(self.canvas)
        self.vertex_marker.setColor(QColor(255, 0, 255))
        self.vertex_marker.setIconSize(11)
        self.vertex_marker.setIconType(QgsVertexMarker.ICON_CROSS)  # or ICON_CROSS, ICON_X, ICON_BOX
        self.vertex_marker.setPenWidth(3)




    def set_project_type(self, project_type):
        self.project_type = project_type


    def edit_add_feature(self, layername):
        """ Button 01, 02: Add 'node' or 'arc' """
                
        # Set active layer and triggers action Add Feature
        layer = QgsMapLayerRegistry.instance().mapLayersByName(layername)
        if layer:
            layer = layer[0]
            self.iface.setActiveLayer(layer)
            layer.startEditing()
            self.iface.actionAddFeature().trigger()
        else:
            self.controller.show_warning("Selected layer name not found: " + str(layername))
        
        
    def edit_arc_topo_repair(self):
        """ Button 19: Topology repair """

        # Uncheck all actions (buttons) except this one
        self.controller.check_actions(False)
        self.controller.check_action(True, 19)
        
        # Create dialog to check wich topology functions we want to execute
        self.dlg = TopologyTools()
        if self.project_type == 'ws':
            self.dlg.tab_review.removeTab(1)
            
        # Set signals
        self.dlg.btn_accept.clicked.connect(self.edit_arc_topo_repair_accept)
        self.dlg.btn_cancel.clicked.connect(self.close_dialog)

        # Manage i18n of the form and open it
        self.controller.translate_form(self.dlg, 'topology_tools')
        self.dlg.exec_()


    def edit_arc_topo_repair_accept(self):
        """ Button 19: Executes functions that are selected """

        # Review/Utils
        if self.dlg.check_node_orphan.isChecked():
            sql = "SELECT "+self.schema_name+".gw_fct_anl_node_orphan();"
            self.controller.execute_sql(sql)
        if self.dlg.check_node_duplicated.isChecked():
            sql = "SELECT "+self.schema_name+".gw_fct_anl_node_duplicated();"
            self.controller.execute_sql(sql)
        if self.dlg.check_topology_coherence.isChecked():
            sql = "SELECT "+self.schema_name+".gw_fct_anl_node_topological_consistency();"
            self.controller.execute_sql(sql)
        if self.dlg.check_arc_same_start_end.isChecked():
            sql = "SELECT "+self.schema_name+".gw_fct_anl_arc_same_startend();"
            self.controller.execute_sql(sql)
        if self.dlg.check_arcs_without_nodes_start_end.isChecked():
            sql = "SELECT "+self.schema_name+".gw_fct_anl_arc_no_startend_node();"
            self.controller.execute_sql(sql)
        if self.dlg.check_connec_duplicated.isChecked():
            sql = "SELECT "+self.schema_name+".gw_fct_anl_connec_duplicated();"
            self.controller.execute_sql(sql)

        # Review/UD
        if self.dlg.check_node_sink.isChecked():
            sql = "SELECT "+self.schema_name+".gw_fct_anl_node_sink();"
            self.controller.execute_sql(sql)
        if self.dlg.check_node_flow_regulator.isChecked():
            sql = "SELECT "+self.schema_name+".gw_fct_anl_node_flowregulator();"
            self.controller.execute_sql(sql)
        if self.dlg.check_node_exit_upper_node_entry.isChecked():
            sql = "SELECT "+self.schema_name+".gw_fct_anl_node_exit_upper_intro();"
            self.controller.execute_sql(sql)
        if self.dlg.check_arc_intersection_without_node.isChecked():
            sql = "SELECT "+self.schema_name+".gw_fct_anl_arc_intersection();"
            self.controller.execute_sql(sql)
        if self.dlg.check_inverted_arcs.isChecked():
            sql = "SELECT "+self.schema_name+".gw_fct_anl_arc_inverted();"
            self.controller.execute_sql(sql)

        # Builder
        if self.dlg.check_create_nodes_from_arcs.isChecked():
            sql = "SELECT "+self.schema_name+".gw_fct_built_nodefromarc();"
            self.controller.execute_sql(sql)

        # Repair
        if self.dlg.check_arc_searchnodes.isChecked():
            sql = "SELECT "+self.schema_name+".gw_fct_repair_arc_searchnodes();"
            self.controller.execute_sql(sql)

        # Close the dialog
        self.close_dialog()

        # Refresh map canvas
        self.iface.mapCanvas().refresh()


    def edit_change_elem_type(self):
        """ Button 28: User select one node. A form is opened showing current node_type.type
            Combo to select new node_type.type
            Combo to select new node_type.id
            Combo to select new cat_node.id
        """

        # Uncheck all actions (buttons) except this one
        self.controller.check_actions(False)
        self.controller.check_action(True, 28)
        
        # Check if any active layer
        layer = self.iface.activeLayer()
        if layer is None:
            message = "You have to select a layer"
            self.controller.show_info(message, context_name='ui_message')
            return

        # Check if at least one node is checked          
        count = layer.selectedFeatureCount()
        if count == 0:
            message = "You have to select at least one feature!"
            self.controller.show_info(message)
            return
        elif count > 1:
            message = "More than one feature selected. Only the first one will be processed!"
            self.controller.show_info(message)

        # Get selected features (nodes)
        feature = layer.selectedFeatures()[0]

        # Create the dialog, fill node_type and define its signals
        self.dlg = ChangeNodeType()
        utils_giswater.setDialog(self.dlg)
        self.new_node_type = self.dlg.findChild(QComboBox, "node_node_type_new")
        self.new_nodecat_id = self.dlg.findChild(QComboBox, "node_nodecat_id")

        # Get node_id and nodetype_id from current node
        self.node_id = feature.attribute('node_id')
        if self.project_type == 'ws':
            node_type = feature.attribute('nodetype_id')
        if self.project_type == 'ud':
            node_type = feature.attribute('node_type')
            sql = "SELECT DISTINCT(id) FROM ud30.cat_node ORDER BY id"
            rows = self.controller.get_rows(sql)
            utils_giswater.fillComboBox(self.new_nodecat_id, rows, allow_nulls=False)

        self.dlg.node_node_type.setText(node_type)
        self.new_node_type.currentIndexChanged.connect(self.edit_change_elem_type_get_value)
        self.dlg.btn_catalog.pressed.connect(partial(self.catalog, self.project_type, 'node'))
        self.dlg.btn_accept.pressed.connect(self.edit_change_elem_type_accept)
        self.dlg.btn_cancel.pressed.connect(self.close_dialog)

        # Fill 1st combo boxes-new system node type
        sql = "SELECT DISTINCT(id) FROM " + self.schema_name + ".node_type ORDER BY id"
        rows = self.dao.get_rows(sql)
        utils_giswater.fillComboBox(self.new_node_type, rows)

        # Manage i18n of the form and open it
        self.controller.translate_form(self.dlg, 'change_node_type')

        self.dlg.exec_()


    def catalog(self, wsoftware, geom_type, node_type=None):
        """ Set dialog depending water software """

        node_type = self.new_node_type.currentText()
        if wsoftware == 'ws':
            self.dlg_cat = WScatalog()
            self.field2 = 'pnom'
            self.field3 = 'dnom'
        elif wsoftware == 'ud':
            self.dlg_cat = UDcatalog()
            self.field2 = 'shape'
            self.field3 = 'geom1'
        utils_giswater.setDialog(self.dlg_cat)
        self.dlg_cat.open()

        # Set signals
        self.dlg_cat.btn_ok.pressed.connect(partial(self.fill_geomcat_id, geom_type))
        self.dlg_cat.btn_cancel.pressed.connect(partial(self.close_dialog, self.dlg_cat))
        self.dlg_cat.matcat_id.currentIndexChanged.connect(partial(self.fill_catalog_id, wsoftware, geom_type))
        self.dlg_cat.matcat_id.currentIndexChanged.connect(partial(self.fill_filter2, wsoftware, geom_type))
        self.dlg_cat.matcat_id.currentIndexChanged.connect(partial(self.fill_filter3, wsoftware, geom_type))
        self.dlg_cat.filter2.currentIndexChanged.connect(partial(self.fill_catalog_id, wsoftware, geom_type))
        self.dlg_cat.filter2.currentIndexChanged.connect(partial(self.fill_filter3, wsoftware, geom_type))
        self.dlg_cat.filter3.currentIndexChanged.connect(partial(self.fill_catalog_id, wsoftware, geom_type))

        self.node_type_text = None
        if wsoftware == 'ws' and geom_type == 'node':
            self.node_type_text = node_type

        sql = "SELECT DISTINCT(matcat_id) as matcat_id "
        sql += " FROM " + self.schema_name + ".cat_" + geom_type
        if wsoftware == 'ws' and geom_type == 'node':
            sql += " WHERE " + geom_type + "type_id = '" + self.node_type_text + "'"
        sql += " ORDER BY matcat_id"
        rows = self.controller.get_rows(sql)
        utils_giswater.fillComboBox(self.dlg_cat.matcat_id, rows)

        sql = "SELECT DISTINCT(" + self.field2 + ")"
        sql += " FROM " + self.schema_name + ".cat_" + geom_type
        if wsoftware == 'ws' and geom_type == 'node':
            sql += " WHERE " + geom_type + "type_id = '" + self.node_type_text + "'"
        sql += " ORDER BY " + self.field2
        rows = self.controller.get_rows(sql)
        utils_giswater.fillComboBox(self.dlg_cat.filter2, rows)

        if wsoftware == 'ws':
            if geom_type == 'node':
                sql = "SELECT " + self.field3
                sql += " FROM (SELECT DISTINCT(regexp_replace(trim(' nm' FROM " + self.field3 + "), '-', '', 'g')::int) as x, " + self.field3
                sql += " FROM " + self.schema_name + ".cat_" + geom_type + " ORDER BY x) AS " + self.field3
            elif geom_type == 'arc':
                sql = "SELECT DISTINCT(" + self.field3 + "), (trim('mm' from " + self.field3 + ")::int) AS x, " + self.field3
                sql += " FROM " + self.schema_name + ".cat_" + geom_type + " ORDER BY x"
            elif geom_type == 'connec':
                sql = "SELECT DISTINCT(TRIM(TRAILING ' ' from " + self.field3 + ")) AS " + self.field3
                sql += " FROM " + self.schema_name + ".cat_" + geom_type + " ORDER BY " + self.field3
        else:
            if geom_type == 'node':
                sql = "SELECT DISTINCT(" + self.field3 + ") AS " + self.field3
                sql += " FROM " + self.schema_name + ".cat_" + geom_type
                sql += " ORDER BY " + self.field3
            elif geom_type == 'arc':
                sql = "SELECT DISTINCT(" + self.field3 + "), (trim('mm' from " + self.field3 + ")::int) AS x, " + self.field3
                sql += " FROM " + self.schema_name + ".cat_" + geom_type + " ORDER BY x"

        rows = self.controller.get_rows(sql)
        utils_giswater.fillComboBox(self.dlg_cat.filter3, rows)


    def fill_filter2(self, wsoftware, geom_type):

        # Get values from filters
        mats = utils_giswater.getWidgetText(self.dlg_cat.matcat_id)

        # Set SQL query
        sql_where = None
        sql = "SELECT DISTINCT(" + self.field2 + ")"
        sql += " FROM " + self.schema_name + ".cat_" + geom_type

        # Build SQL filter
        if mats != "null":
            if sql_where is None:
                sql_where = " WHERE"
            sql_where += " matcat_id = '" + mats + "'"
        if wsoftware == 'ws' and self.node_type_text is not None:
            if sql_where is None:
                sql_where = " WHERE"
            else:
                sql_where += " AND"
            sql_where += " " + geom_type + "type_id = '" + self.node_type_text + "'"
        sql += sql_where + " ORDER BY " + self.field2

        rows = self.controller.get_rows(sql)
        utils_giswater.fillComboBox(self.dlg_cat.filter2, rows)
        self.fill_filter3(wsoftware, geom_type)


    def fill_filter3(self, wsoftware, geom_type):

        # Get values from filters
        mats = utils_giswater.getWidgetText(self.dlg_cat.matcat_id)
        filter2 = utils_giswater.getWidgetText(self.dlg_cat.filter2)

        # Set SQL query
        sql_where = None
        if wsoftware == 'ws' and geom_type != 'connec':
            sql = "SELECT " + self.field3
            sql += " FROM (SELECT DISTINCT(regexp_replace(trim(' nm'from " + self.field3 + "),'-','', 'g')::int) as x, " + self.field3
        elif wsoftware == 'ws' and geom_type == 'connec':
            sql = "SELECT DISTINCT(TRIM(TRAILING ' ' from " + self.field3 + ")) as " + self.field3
        else:
            sql = "SELECT DISTINCT(" + self.field3 + ")"
        sql += " FROM " + self.schema_name + ".cat_" + geom_type

        # Build SQL filter
        if wsoftware == 'ws' and self.node_type_text is not None:
            sql_where = " WHERE " + geom_type + "type_id = '" + self.node_type_text + "'"
        if mats != "null":
            if sql_where is None:
                sql_where = " WHERE"
            else:
                sql_where += " AND"
            sql_where += " matcat_id = '" + mats + "'"
        if filter2 != "null":
            if sql_where is None:
                sql_where = " WHERE"
            else:
                sql_where += " AND"
            sql_where += " " + self.field2 + " = '" + filter2 + "'"
        if wsoftware == 'ws' and geom_type != 'connec':
            sql += sql_where + " ORDER BY x) AS " + self.field3
        else:
            sql += sql_where + " ORDER BY " + self.field3

        rows = self.controller.get_rows(sql)
        utils_giswater.fillComboBox(self.dlg_cat.filter3, rows)


    def fill_catalog_id(self, wsoftware, geom_type):

        # Get values from filters
        mats = utils_giswater.getWidgetText(self.dlg_cat.matcat_id)
        filter2 = utils_giswater.getWidgetText(self.dlg_cat.filter2)
        filter3 = utils_giswater.getWidgetText(self.dlg_cat.filter3)

        # Set SQL query
        sql_where = None
        sql = "SELECT DISTINCT(id) as id"
        sql += " FROM " + self.schema_name + ".cat_" + geom_type

        if wsoftware == 'ws' and self.node_type_text is not None:
            sql_where = " WHERE " + geom_type + "type_id = '" + self.node_type_text + "'"
        if mats != "null":
            if sql_where is None:
                sql_where = " WHERE"
            else:
                sql_where += " AND"
            sql_where += " matcat_id = '" + mats + "'"
        if filter2 != "null":
            if sql_where is None:
                sql_where = " WHERE"
            else:
                sql_where += " AND"
            sql_where += " " + self.field2 + " = '" + filter2 + "'"
        if filter3 != "null":
            if sql_where is None:
                sql_where = " WHERE"
            else:
                sql_where += " AND"
            sql_where += " " + self.field3 + " = '" + filter3 + "'"
        sql += sql_where + " ORDER BY id"

        rows = self.controller.get_rows(sql)
        utils_giswater.fillComboBox(self.dlg_cat.id, rows)


    def fill_geomcat_id(self, geom_type):
        catalog_id = utils_giswater.getWidgetText(self.dlg_cat.id)
        self.close_dialog(self.dlg_cat)
        self.new_nodecat_id.setEnabled(True)
        utils_giswater.setWidgetText(self.new_nodecat_id, catalog_id)


    def edit_add_element(self):
        """ Button 33: Add element """

        # Uncheck all actions (buttons) except this one
        #self.controller.check_actions(False)

        # Remove all previous selections
        #self.remove_selection()
        # TODO : parametrizide list of layers
        self.group_layers_arc = ["Pipe", "Varc"]
        self.group_pointers_arc = []
        for layer in self.group_layers_arc:
            self.group_pointers_arc.append(QgsMapLayerRegistry.instance().mapLayersByName(layer)[0])

        self.group_layers_node = ["Junction", "Valve", "Manhole", "Tank", "Source", "Pump", "Hydrant", "Waterwell",
                                  "Meter", "Reduction", "Filter"]
        self.group_pointers_node = []
        for layer in self.group_layers_node:
            self.group_pointers_node.append(QgsMapLayerRegistry.instance().mapLayersByName(layer)[0])

        self.group_layers_connec = ["Wjoin", "Greentap", "Fountain", "Tap"]
        self.group_pointers_connec = []
        for layer in self.group_layers_connec:
            self.group_pointers_connec.append(QgsMapLayerRegistry.instance().mapLayersByName(layer)[0])
        self.ids = []
        self.ids_arc = []
        self.ids_node = []
        self.ids_connec = []
        self.x = ""
        self.y = ""
        # Create the dialog and signals
        self.dlg = AddElement()
        utils_giswater.setDialog(self.dlg)
        self.set_icon(self.dlg.add_geom, "133")
        self.set_icon(self.dlg.btn_insert, "111")
        self.set_icon(self.dlg.btn_delete, "112")
        self.set_icon(self.dlg.btn_snapping, "137")
        self.dlg.btn_accept.pressed.connect(self.ed_add_element_accept)
        self.dlg.btn_cancel.pressed.connect(self.close_dialog)

        # Manage i18n of the form
        self.controller.translate_form(self.dlg, 'element')

        # Check if we have at least one feature selected
        #if not self.edit_check():
        #    return

        # Adding auto-completion to a QLineEdit - element_id
        self.completer = QCompleter()
        self.dlg.element_id.setCompleter(self.completer)
        model = QStringListModel()

        sql = "SELECT DISTINCT(element_id) FROM " + self.schema_name + ".element"
        rows = self.controller.get_rows(sql)
        values = []
        for row in rows:
            values.append(str(row[0]))

        model.setStringList(values)
        self.completer.setModel(model)
        # Fill combo boxes
        self.populate_combo("elementcat_id", "cat_element")
        self.populate_combo("state", "value_state", "name")
        self.populate_combo("expl_id", "exploitation", "name")
        self.populate_combo("location_type", "man_type_location")
        self.populate_combo("workcat_id", "cat_work")
        self.populate_combo("buildercat_id", "cat_builder")
        self.populate_combo("ownercat_id", "cat_owner")
        self.populate_combo("verified", "value_verified")
        self.populate_combo("workcat_id_end", "cat_work")


        # SET DEFAULT - TAB0
        # Set default tab 0
        self.tab_feature = self.dlg.findChild(QTabWidget, "tab_feature")
        if self.project_type == 'ws':
            self.tab_feature.removeTab(3)

        # if self.project_type == 'ud':

        self.tab_feature.setCurrentIndex(0)
        # Set default values
        feature = "arc"
        table = "element_x_arc"
        view = "v_edit_arc"

        # Check which tab is selected
        table = "element"
        self.tab_feature.currentChanged.connect(partial(self.set_feature,table))
        self.dlg.element_id.textChanged.connect(partial(self.check_el_exist, "element_id", table))

        # Adding auto-completion to a QLineEdit for default feature
        self.init_add_element(feature, table, view)
        # Set signal to reach selected value from QCompleter
        # self.completer.activated.connect(self.ed_add_el_autocomplete)
        self.dlg.add_geom.pressed.connect(self.add_point)


        self.widget = self.dlg.findChild(QTableView, "tbl_doc_x_arc")

        #self.dlg.btn_insert.pressed.connect(partial(self.manual_init_update, self.ids_arc, "arc_id", self.group_pointers_arc))
        self.dlg.btn_insert.pressed.connect(partial(self.manual_init, self.widget, view, feature + "_id", self.dlg, self.group_pointers_arc))
        self.dlg.btn_delete.pressed.connect(partial(self.delete_records, self.widget, view, feature + "_id", self.group_pointers_arc))
        self.dlg.btn_snapping.pressed.connect(partial(self.snapping_init, self.group_pointers_arc, self.group_layers_arc, feature + "_id", view))

        # Open the dialog
        self.dlg.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.dlg.open()


    def check_doc_exist(self, attribute, table):

        id_ = self.dlg.doc_id.text()

        # Check if we already have data with selected element_id
        sql = "SELECT DISTINCT(" + str(attribute) + ") FROM " + self.schema_name + "." + str(table) + " WHERE " + str(
            attribute) + " = '" + str(id_) + "'"
        row = self.dao.get_row(sql)

        if row:
            # If element exist : load data ELEMENT
            sql = "SELECT * FROM " + self.schema_name + "." + table + " WHERE " + attribute + " = '" + str(id_) + "'"
            row = self.dao.get_row(sql)

            utils_giswater.setWidgetText("doc_type", row['doc_type'])
            self.dlg.observ.setText(str(row['observ']))
            self.dlg.path.setText(str(row['path']))

            self.ids_node = []
            self.ids_arc = []
            self.ids_connec = []
            self.ids = []
            # If element exist : load data RELATIONS

            sql = "SELECT arc_id FROM " + self.schema_name + ".doc_x_arc WHERE doc_id = '" + str(id_) + "'"
            rows = self.controller.get_rows(sql)

            if rows:
                for row in rows:
                    self.ids_arc.append(str(row[0]))
                    self.ids.append(str(row[0]))

                self.manual_init_update(self.ids_arc, "arc_id", self.group_pointers_arc)
                self.reload_table_update("v_edit_arc", "arc_id", self.ids_arc, self.dlg.tbl_doc_x_arc)

            sql = "SELECT node_id FROM " + self.schema_name + ".doc_x_node WHERE doc_id = '" + str(id_) + "'"
            rows = self.controller.get_rows(sql)

            if rows:
                for row in rows:
                    self.ids_node.append(str(row[0]))
                    self.ids.append(str(row[0]))

                self.manual_init_update(self.ids_node, "node_id", self.group_pointers_node)
                self.reload_table_update("v_edit_node", "node_id", self.ids_node, self.dlg.tbl_doc_x_node)

            sql = "SELECT connec_id FROM " + self.schema_name + ".doc_x_connec WHERE doc_id = '" + str(id_) + "'"
            rows = self.controller.get_rows(sql)

            if rows:
                for row in rows:
                    self.ids_connec.append(str(row[0]))
                    self.ids.append(str(row[0]))

                self.reload_table_update("v_edit_connec", "connec_id", self.ids_connec, self.dlg.tbl_doc_x_connec)
                self.manual_init_update(self.ids_connec, "connec_id", self.group_pointers_connec)

        if not row:
            # If element_id not exiast : Clear data
            utils_giswater.setWidgetText("doc_type", str(""))
            self.dlg.observ.setText(str(""))
            self.dlg.path.setText(str(""))
            return


    def check_el_exist(self,attribute,table):

        id_ = self.dlg.element_id.text()

        # Check if we already have data with selected element_id
        sql = "SELECT DISTINCT(" + str(attribute) + ") FROM " + self.schema_name + "." + str(table) + " WHERE " + str(attribute) + " = '" + str(id_) + "'"
        row = self.dao.get_row(sql)

        if row:
            # If element exist : load data ELEMENT
            sql = "SELECT * FROM " + self.schema_name + "."+ table+" WHERE " + attribute + " = '" + str(id_) + "'"
            row = self.dao.get_row(sql)
            # Set data
            utils_giswater.setWidgetText("elementcat_id", row['elementcat_id'])

            # TODO make join
            if str(row['state']) == '0':
                state = "OBSOLETE"
            if str(row['state']) == '1':
                state = "ON SERVICE"
            if str(row['state']) == '2':
                state = "PLANIFIED"

            if str(row['expl_id']) == '1':
                expl_id = "expl_01"
            if str(row['expl_id']) == '2':
                expl_id = "expl_02"
            if str(row['expl_id']) == '3':
                expl_id = "expl_03"
            if str(row['expl_id']) == '4':
                expl_id = "expl_03"

            utils_giswater.setWidgetText("state", str(state))
            utils_giswater.setWidgetText("expl_id", str(expl_id))
            utils_giswater.setWidgetText("ownercat_id", row['ownercat_id'])
            utils_giswater.setWidgetText("location_type", row['location_type'])
            utils_giswater.setWidgetText("buildercat_id", row['buildercat_id'])
            utils_giswater.setWidgetText("workcat_id", row['workcat_id'])
            utils_giswater.setWidgetText("workcat_id_end", row['workcat_id_end'])
            self.dlg.comment.setText(str(row['comment']))
            self.dlg.observ.setText(str(row['observ']))
            self.dlg.path.setText(str(row['link']))
            utils_giswater.setWidgetText("verified", row['verified'])
            self.dlg.rotation.setText(str(row['rotation']))
            if str(row['undelete'])== 'True':
                self.dlg.undelete.setChecked(True)
            builtdate = QDate.fromString(str(row['builtdate']), 'yyyy-MM-dd')
            enddate = QDate.fromString(str(row['enddate']), 'yyyy-MM-dd')

            self.dlg.builtdate.setDate(builtdate)
            self.dlg.enddate.setDate(enddate)


            self.ids_node = []
            self.ids_arc = []
            self.ids_connec = []
            self.ids = []
            # If element exist : load data RELATIONS

            sql = "SELECT arc_id FROM " + self.schema_name + ".element_x_arc WHERE element_id = '" + str(id_) + "'"
            rows = self.controller.get_rows(sql)
            if rows:
                for row in rows:
                    self.ids_arc.append(str(row[0]))
                    self.ids.append(str(row[0]))

                self.manual_init_update(self.ids_arc, "arc_id", self.group_pointers_arc)
                self.reload_table_update("v_edit_arc", "arc_id", self.ids_arc, self.dlg.tbl_doc_x_arc)


            sql = "SELECT node_id FROM " + self.schema_name + ".element_x_node WHERE element_id = '" + str(id_) + "'"
            rows = self.controller.get_rows(sql)
            if rows:
                for row in rows:
                    self.ids_node.append(str(row[0]))
                    self.ids.append(str(row[0]))

                self.manual_init_update(self.ids_node, "node_id", self.group_pointers_node)
                self.reload_table_update("v_edit_node", "node_id", self.ids_node, self.dlg.tbl_doc_x_node)


            sql = "SELECT connec_id FROM " + self.schema_name + ".element_x_connec WHERE element_id = '" + str(id_) + "'"
            rows = self.controller.get_rows(sql)
            if rows:
                for row in rows:
                    self.ids_connec.append(str(row[0]))
                    self.ids.append(str(row[0]))

                self.reload_table_update("v_edit_connec", "connec_id", self.ids_connec, self.dlg.tbl_doc_x_connec)
                self.manual_init_update(self.ids_connec, "connec_id", self.group_pointers_connec)


        if not row:
            # If element_id not exiast : Clear data
            utils_giswater.setWidgetText("elementcat_id", str(""))
            utils_giswater.setWidgetText("state", str(""))
            utils_giswater.setWidgetText("expl_id",str(""))
            utils_giswater.setWidgetText("ownercat_id", str(""))
            utils_giswater.setWidgetText("location_type", str(""))
            utils_giswater.setWidgetText("buildercat_id", str(""))
            utils_giswater.setWidgetText("workcat_id", str(""))
            utils_giswater.setWidgetText("workcat_id_end", str(""))
            self.dlg.comment.setText(str(""))
            self.dlg.observ.setText(str(""))
            self.dlg.path.setText(str(""))
            utils_giswater.setWidgetText("verified", str(""))
            self.dlg.rotation.setText(str(""))
            return


    def set_feature(self, table):

        self.dlg.btn_insert.pressed.disconnect()
        self.dlg.btn_delete.pressed.disconnect()
        self.dlg.btn_snapping.pressed.disconnect()

        self.emit_point = QgsMapToolEmitPoint(self.canvas)
        self.canvas.setMapTool(self.emit_point)

        tab_position = self.tab_feature.currentIndex()

        if tab_position == 0:
            feature = "arc"
            table = table + "_x_arc"
            view = "v_edit_arc"
            group_pointers = self.group_pointers_arc
            group_layers = self.group_layers_arc
            layer = QgsMapLayerRegistry.instance().mapLayersByName("Edit arc")[0]
            self.iface.setActiveLayer(layer)
            self.widget = self.dlg.findChild(QTableView, "tbl_doc_x_arc")
        if tab_position == 1:
            feature = "node"
            table = table + "_x_node"
            view = "v_edit_node"
            group_pointers = self.group_pointers_node
            group_layers = self.group_layers_node
            layer = QgsMapLayerRegistry.instance().mapLayersByName("Edit node")[0]
            self.iface.setActiveLayer(layer)
            self.widget = self.dlg.findChild(QTableView, "tbl_doc_x_node")
        if tab_position == 2:
            feature = "connec"
            table = table + "_x_connec"
            view = "v_edit_connec"
            group_pointers = self.group_pointers_connec
            group_layers = self.group_layers_connec
            layer = QgsMapLayerRegistry.instance().mapLayersByName("Edit connec")[0]
            self.iface.setActiveLayer(layer)
            self.widget = self.dlg.findChild(QTableView, "tbl_doc_x_connec")

        if tab_position == 3:
            # TODO : check project if WS-delete gully tab if UD-set parameters
            feature = "gully"
            table = "element_x_gully"
            view = "v_edit_gully"


        # Adding auto-completion to a QLineEdit
        self.init_add_element(feature, table, view)

        self.dlg.btn_insert.pressed.connect(partial(self.manual_init, self.widget, view, feature + "_id", self.dlg, group_pointers))
        self.dlg.btn_delete.pressed.connect(partial(self.delete_records, self.widget, view, feature + "_id",  group_pointers))
        self.dlg.btn_snapping.pressed.connect(partial(self.snapping_init, group_pointers,group_layers, feature + "_id",view))



    def init_add_element(self, feature, table, view):

        # Adding auto-completion to a QLineEdit
        self.edit = self.dlg.findChild(QLineEdit, "feature_id")
        self.completer = QCompleter()
        self.edit.setCompleter(self.completer)
        model = QStringListModel()

        #sql = "SELECT DISTINCT(element_id) FROM " + self.schema_name + ".element "
        sql = "SELECT " + feature + "_id FROM " + self.schema_name + "."+view
        row = self.dao.get_rows(sql)
        for i in range(0, len(row)):
            aux = row[i]
            row[i] = str(aux[0])

        model.setStringList(row)
        self.completer.setModel(model)


    def manual_init(self, widget, table, attribute, dialog, group_pointers) :
        '''  Select feature with entered id
        Set a model with selected filter.
        Attach that model to selected table '''
        widget_feature_id = self.dlg.findChild(QLineEdit, "feature_id")
        element_id = widget_feature_id.text()
        # Clear list of ids
        self.ids = []
        for layer in group_pointers:
            if layer.selectedFeatureCount() > 0:
                # Get all selected features at layer
                features = layer.selectedFeatures()
                # Get id from all selected features
                for feature in features:
                    feature_id = feature.attribute(attribute)
                    # List of all selected features
                    self.ids.append(str(feature_id))

        # Check if user entered hydrometer_id
        if element_id == "":
            message = "You need to enter id"
            self.controller.show_info_box(message)
            return
        if element_id in self.ids:
            message = str(attribute)+ ":"+element_id+" id already in the list!"
            return
        else:
            # If feature id doesn't exist in list -> add
            self.ids.append(element_id)
            # SELECT features which are in the list
        aux = attribute + " IN ("
        for i in range(len(self.ids)):
            aux += "'" + str(self.ids[i]) + "', "
        aux = aux[:-2] + ")"
        expr = QgsExpression(aux)
        if expr.hasParserError():
            message = "Expression Error: " + str(expr.parserErrorString())
            self.controller.show_warning(message)
            return

        for layer in group_pointers:

            it = layer.getFeatures(QgsFeatureRequest(expr))
            # Build a list of feature id's from the previous result
            id_list = [i.id() for i in it]
            # Select features with these id's
            layer.setSelectedFeatures(id_list)

        # Reload table
        self.reload_table(table, attribute)


    def manual_init_update(self, ids, attribute, group_pointers) :
        '''  Select feature with entered id
        Set a model with selected filter.
        Attach that model to selected table '''

        if len(ids) > 0 :
            aux = attribute + " IN ("
            for i in range(len(ids)):
                aux += "'" + str(ids[i]) + "', "
            aux = aux[:-2] + ")"
            expr = QgsExpression(aux)
            if expr.hasParserError():
                message = "Expression Error: " + str(expr.parserErrorString())
                self.controller.show_warning(message)
                return

        for layer in group_pointers:
            # SELECT features which are in the list
            it = layer.getFeatures(QgsFeatureRequest(expr))
            # Build a list of feature id's from the previous result
            id_list = [i.id() for i in it]
            # Select features with these id's
            layer.setSelectedFeatures(id_list)


    def snapping_init(self, group_pointers, group_layers, attribute, view):
        #btn_snapping

        self.tool = MultipleSnapping(self.iface, self.settings, self.controller, self.plugin_dir, group_layers)
        self.canvas.setMapTool(self.tool)

        # Disconnect previous
        #self.canvas.disconnect(self.canvas, SIGNAL("xyCoordinates(const QgsPoint&)"), self.mouse_move)
        #self.iface.mapCanvas().selectionChanged.disconnect(self.snapping_selection)

        self.canvas.connect(self.canvas, SIGNAL("xyCoordinates(const QgsPoint&)"), self.mouse_move)
        #self.iface.mapCanvas().selectionChanged.disconnect()
        self.iface.mapCanvas().selectionChanged.connect(partial(self.snapping_selection, group_pointers, attribute,view))


    def mouse_move(self, p):

        map_point = self.canvas.getCoordinateTransform().transform(p)
        x = map_point.x()
        y = map_point.y()
        eventPoint = QPoint(x, y)

        # Snapping
        # (retval, result) = self.snapper.snapToBackgroundLayers(eventPoint)  # @UnusedVariable
        (retval, result) = self.snapper.snapToCurrentLayer(eventPoint, 2)  # @UnusedVariable

        # That's the snapped point
        if result <> []:
            point = QgsPoint(result[0].snappedVertex)
            self.vertex_marker.setCenter(point)
            self.vertex_marker.show()
        else:
            self.vertex_marker.hide()


    def snapping_selection(self, group_pointers, attribute, view):

        self.ids = []
        for layer in group_pointers:
            if layer.selectedFeatureCount() > 0:

                # Get all selected features at layer
                features = layer.selectedFeatures()
                # Get id from all selected features
                for feature in features:
                    element_id = feature.attribute(attribute)
                    # Add element
                    if element_id in self.ids:
                        message = " Feature :" + element_id + " id already in the list!"
                        self.controller.show_info_box(message)
                        return
                    else:
                        self.ids.append(element_id)

        if attribute == 'arc_id':
            self.ids_arc = self.ids
            self.reload_table_update("v_edit_arc", "arc_id", self.ids_arc, self.dlg.tbl_doc_x_arc)
        if attribute == 'node_id':
            self.ids_node = self.ids
            self.reload_table_update("v_edit_node", "node_id", self.ids_node, self.dlg.tbl_doc_x_node)
        if attribute == 'connec_id':
            self.ids_connec = self.ids
            self.reload_table_update("v_edit_connec", "connec_id", self.ids_connec, self.dlg.tbl_doc_x_connec)


    def reload_table(self, table, attribute):
        # Reload table
        table_name = self.schema_name + "." + table
        widget = self.widget

        expr = attribute+"= '" + str(self.ids[0]) + "'"
        if len(self.ids) > 1:
            for el in range(1, len(self.ids)):
                expr += " OR "+attribute+" = '" + str(self.ids[el]) + "'"

        # Set model
        model = QSqlTableModel();
        model.setTable(table_name)
        model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        model.select()

        # Check for errors
        if model.lastError().isValid():
            self.controller.show_warning(model.lastError().text())

        # Attach model to table view
        widget.setModel(model)
        widget.model().setFilter(expr)
        widget.model().select()


    def reload_table_update(self, table, attribute, ids, widget):

        # Reload table
        table_name = self.schema_name + "." + table
        expr = attribute + "= '" + str(ids[0]) + "'"

        if len(ids) > 1:
            for el in range(1, len(ids)):
                expr += " OR " + str(attribute) + " = '" + str(ids[el]) + "'"

        # Set model
        model = QSqlTableModel();
        model.setTable(table_name)
        model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        model.select()

        # Check for errors
        if model.lastError().isValid():
            self.controller.show_warning(model.lastError().text())

        # Attach model to table view
        widget.setModel(model)
        widget.model().setFilter(expr)


    def remove_selection(self):
        ''' Remove all previous selections'''

        for layer in self.canvas.layers():
            layer.removeSelection()
        self.canvas.refresh()


    def delete_records(self, widget, table_name, id_, group_pointers):
        ''' Delete selected elements of the table '''
        tab_position = self.tab_feature.currentIndex()

        if tab_position == 0:
            self.ids = self.ids_arc

        if tab_position == 1:
            self.ids = self.ids_node

        if tab_position == 2:
            self.ids = self.ids_connec

        # Get selected rows
        selected_list = widget.selectionModel().selectedRows()
        if len(selected_list) == 0:
            message = "Any record selected"
            self.controller.show_info_box(message)
            return

        del_id = []
        inf_text = ""
        list_id = ""
        for i in range(0, len(selected_list)):
            row = selected_list[i].row()
            id_feature = widget.model().record(row).value(id_)
            inf_text += str(id_feature) + ", "
            list_id = list_id + "'" + str(id_feature) + "', "
            del_id.append(id_feature)
        inf_text = inf_text[:-2]
        list_id = list_id[:-2]
        answer = self.controller.ask_question("Are you sure you want to delete these records?", "Delete records", inf_text)

        if answer:
            for el in del_id:
                self.ids.remove(el)

                if tab_position == 0:
                    sql = "DELETE FROM " + self.schema_name + ".element_x_arc WHERE arc_id ='" + str(el) + "'"
                    ids = self.ids_arc
                    #self.ids_arc.remove(str(el))
                if tab_position == 1:
                    sql = "DELETE FROM " + self.schema_name + ".element_x_node WHERE node_id ='" + str(el) + "'"
                    ids = self.ids_node
                    #self.ids_node.remove(str(el))
                if tab_position == 2:
                    sql = "DELETE FROM " + self.schema_name + ".element_x_connec WHERE connec_id ='" + str(el) + "'"
                    ids = self.ids_connec


        ids = self.ids
        # Reload selection
        #layer = self.iface.activeLayer()

        for layer in group_pointers:
            # SELECT features which are in the list
            aux = "\""+str(id_)+"\" IN ("
            for i in range(len(ids)):
                aux += "'" + str(ids[i]) + "', "
            aux = aux[:-2] + ")"

            expr = QgsExpression(aux)
            if expr.hasParserError():
                message = "Expression Error: " + str(expr.parserErrorString())
                self.controller.show_warning(message)
                return
            it = layer.getFeatures(QgsFeatureRequest(expr))

            # Build a list of feature id's from the previous result
            id_list = [i.id() for i in it]

            # Select features with these id's
            layer.setSelectedFeatures(id_list)


            # Reload table
            expr = str(id_)+" = '" + ids[0] + "'"
            if len(ids) > 1:
                for i in range(1, len(ids)):
                    expr += " OR "+str(id_)+ "= '" + ids[i] + "'"

            widget.model().setFilter(expr)
            widget.model().select()


    def edit_add_file(self):
        """ Button 34: Add document """

        # Uncheck all actions (buttons) except this one
        #self.controller.check_actions(False)
        # Remove all previous selections
        #self.remove_selection()
        # TODO : parametrizide list of layers
        self.group_layers_arc = ["Pipe", "Varc"]
        self.group_pointers_arc = []
        for layer in self.group_layers_arc:
            self.group_pointers_arc.append(QgsMapLayerRegistry.instance().mapLayersByName(layer)[0])

        self.group_layers_node = ["Junction", "Valve", "Manhole", "Tank", "Source", "Pump", "Hydrant", "Waterwell",
                                  "Meter", "Reduction", "Filter"]
        self.group_pointers_node = []
        for layer in self.group_layers_node:
            self.group_pointers_node.append(QgsMapLayerRegistry.instance().mapLayersByName(layer)[0])

        self.group_layers_connec = ["Wjoin", "Greentap", "Fountain", "Tap"]
        self.group_pointers_connec = []
        for layer in self.group_layers_connec:
            self.group_pointers_connec.append(QgsMapLayerRegistry.instance().mapLayersByName(layer)[0])

        self.ids = []
        self.ids_arc = []
        self.ids_node = []
        self.ids_connec = []
        self.x = ""
        self.y = ""

        # Create the dialog and signals
        self.dlg = AddDoc()
        utils_giswater.setDialog(self.dlg)

        self.tab_feature = self.dlg.findChild(QTabWidget, "tab_feature")
        if self.project_type == 'ws':
            self.tab_feature.removeTab(3)

        #self.set_icon(self.dlg.add_geom, "129")
        self.set_icon(self.dlg.btn_insert, "111")
        self.set_icon(self.dlg.btn_delete, "112")
        self.set_icon(self.dlg.btn_snapping, "137")

        self.dlg.btn_accept.pressed.connect(self.edit_add_file_accept)
        self.dlg.btn_cancel.pressed.connect(self.close_dialog)

        # Get widgets
        self.dlg.path_url.clicked.connect(partial(self.open_web_browser, "path"))
        self.dlg.path_doc.clicked.connect(partial(self.get_file_dialog, "path"))

        # Manage i18n of the form
        self.controller.translate_form(self.dlg, 'file')

        # Check if we have at least one feature selected
        #if not self.edit_check():
        #    return

        # Fill combo boxes
        self.populate_combo("doc_type", "doc_type")

        # Adding auto-completion to a QLineEdit
        self.completer = QCompleter()
        self.dlg.doc_id.setCompleter(self.completer)

        model = QStringListModel()
        sql = "SELECT DISTINCT(id) FROM " + self.schema_name + ".doc "
        row = self.dao.get_rows(sql)
        for i in range(0, len(row)):
            aux = row[i]
            row[i] = str(aux[0])

        model.setStringList(row)
        self.completer.setModel(model)

        # SET DEFAULT - TAB0
        # Set default tab 0
        self.tab_feature = self.dlg.findChild(QTabWidget, "tab_feature")
        self.tab_feature.setCurrentIndex(0)
        # Set default values
        feature = "arc"
        table = "doc_x_arc"
        view = "v_edit_arc"

        # Check which tab is selected
        table = "doc"
        self.tab_feature.currentChanged.connect(partial(self.set_feature,table))
        self.dlg.doc_id.textChanged.connect(partial(self.check_doc_exist, "id", table))


        # Adding auto-completion to a QLineEdit for default feature
        self.init_add_element(feature, table, view)


        self.widget = self.dlg.findChild(QTableView, "tbl_doc_x_arc")
        self.dlg.btn_insert.pressed.connect(partial(self.manual_init, self.widget, view, feature + "_id", self.dlg, self.group_pointers_arc))
        self.dlg.btn_delete.pressed.connect(partial(self.delete_records, self.widget, view, feature + "_id", self.group_pointers_arc))
        self.dlg.btn_snapping.pressed.connect(partial(self.snapping_init, self.group_pointers_arc, self.group_layers_arc, feature + "_id", view))

        # Open the dialog
        self.dlg.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.dlg.open()


    def edit_change_elem_type_get_value(self, index):
        """ Just select item to 'real' combo 'nodecat_id' (that is hidden) """
        if index == -1:
            return

        # Get selected value from 2nd combobox
        node_node_type_new = utils_giswater.getWidgetText(self.new_node_type)

        # When value is selected, enabled 3rd combo box
        if node_node_type_new != 'null':
            # Get selected value from 2nd combobox
            utils_giswater.setWidgetEnabled(self.new_nodecat_id)

            # Fill 3rd combo_box-catalog_id
            sql = "SELECT DISTINCT(id)"
            sql += " FROM " + self.schema_name + ".cat_node"
            sql += " WHERE nodetype_id = '" + node_node_type_new + "'"
            rows = self.dao.get_rows(sql)
            utils_giswater.fillComboBox(self.new_nodecat_id, rows)


    def edit_change_elem_type_accept(self):
        """ Update current type of node and save changes in database """

        old_node_type = utils_giswater.getWidgetText("node_node_type")
        node_node_type_new = utils_giswater.getWidgetText("node_node_type_new")
        node_nodecat_id = utils_giswater.getWidgetText("node_nodecat_id")

        if node_node_type_new != "null":
            if (node_nodecat_id != "null" and self.project_type == 'ws') or (self.project_type == 'ud'):
                sql = "SELECT man_table FROM  " + self.schema_name + ".node_type WHERE id = '" + old_node_type + "'"
                row = self.controller.get_row(sql)
                if not row:
                    return

                # Delete from current table
                sql = "DELETE FROM "+self.schema_name + "." + row[0] + " WHERE node_id ='" + self.node_id + "'"
                self.controller.execute_sql(sql)

                sql = "SELECT man_table FROM "+self.schema_name + ".node_type WHERE id ='" + node_node_type_new + "'"
                row = self.controller.get_row(sql)
                if not row:
                    return

                # Insert into new table
                sql = "INSERT INTO " + self.schema_name + "." + row[0] + "(node_id)"
                sql += " VALUES (" + self.node_id + ")"
                self.controller.execute_sql(sql)

                # Update field 'nodecat_id'
                if self.project_type == 'ws':
                    sql = "UPDATE " + self.schema_name + ".node SET nodecat_id = '" + node_nodecat_id + "'"
                    sql += " WHERE node_id = '" + self.node_id + "'"
                    self.controller.execute_sql(sql)
                # TODO  mirar si el  ""and node_nodecat_id != ''"" hace falta, ya que ahora el combobox no tendra registro vacio
                if self.project_type == 'ud':
                    sql = "UPDATE " + self.schema_name + ".node SET nodecat_id = '" + node_nodecat_id + "'"
                    sql += " WHERE node_id = '" + self.node_id + "'"
                    self.controller.execute_sql(sql)
                    sql = "UPDATE " + self.schema_name + ".node SET node_type = '" + node_node_type_new + "'"
                    sql += " WHERE node_id = '" + self.node_id + "'"
                    self.controller.execute_sql(sql)
            else:
                message = "Field catalog_id required!"
                self.controller.show_warning(message)
        else:
            message = "The node has not been updated because no catalog has been selected!"
            self.controller.show_warning(message)

        # Close form
        self.close_dialog(self.dlg)


    def edit_add_file_autocomplete(self):
        """ Once we select 'element_id' using autocomplete, fill widgets with current values """

        self.dlg.doc_id.setCompleter(self.completer)
        doc_id = utils_giswater.getWidgetText("doc_id")

        # Get values from database
        sql = "SELECT doc_type, tagcat_id, observ, path"
        sql += " FROM " + self.schema_name + ".doc"
        sql += " WHERE id = '" + doc_id + "'"
        row = self.dao.get_row(sql)

        # Fill widgets
        columns_length = self.dao.get_columns_length()
        for i in range(0, columns_length):
            column_name = self.dao.get_column_name(i)
            utils_giswater.setWidgetText(column_name, row[column_name])


    def edit_add_file_accept(self):
        """ Insert or update table 'document'. Add document to selected feature """

        # Get values from dialog
        doc_id = utils_giswater.getWidgetText("doc_id")
        doc_type = utils_giswater.getWidgetText("doc_type")
        observ = utils_giswater.getWidgetText("observ")
        path = utils_giswater.getWidgetText("path")

        if doc_id == 'null':
            # Show warning message
            message = "You need to insert doc_id"
            self.controller.show_warning(message, context_name='ui_message')
            return

        # Check if this document already exists
        sql = "SELECT DISTINCT(id) FROM " + self.schema_name + ".doc WHERE id = '" + doc_id + "'"
        row = self.dao.get_row(sql)
        
        # If document already exist perform an UPDATE
        if row:
            answer = self.controller.ask_question("Are you sure you want change the data?")
            if answer:
                sql = "UPDATE " + self.schema_name + ".doc "
                sql += " SET doc_type = '" + doc_type + "', observ = '" + observ + "', path = '" + path + "'"
                sql += " WHERE id = '" + doc_id + "'"
                status = self.controller.execute_sql(sql)
                if status:
                    #self.ed_add_to_feature("doc", doc_id)
                    message = "Values has been updated"
                    self.controller.show_info(message, context_name='ui_message')

                message = "Values has been updated into table document"
                self.controller.show_info(message)

                sql = "DELETE FROM " + self.schema_name + ".doc_x_node WHERE  doc_id = '" + str(doc_id) + "'"
                self.controller.execute_sql(sql)
                sql = "DELETE FROM " + self.schema_name + ".doc_x_arc WHERE  doc_id = '" + str(doc_id) + "'"
                self.controller.execute_sql(sql)
                sql = "DELETE FROM " + self.schema_name + ".doc_x_connec WHERE  doc_id = '" + str(doc_id) + "'"
                self.controller.execute_sql(sql)

                if self.ids_arc != []:

                    for arc_id in self.ids_arc:
                        sql = "INSERT INTO " + self.schema_name + ".doc_x_arc (doc_id, arc_id )"
                        sql += " VALUES ('" + str(doc_id) + "', '" + str(arc_id) + "')"
                        status = self.controller.execute_sql(sql)
                        if status:
                            message = "Values has been updated into table doc_x_arc"
                            self.controller.show_info(message)
                        if not status:
                            message = "Error inserting element in table, you need to review data"
                            self.controller.show_warning(message)
                            return
                if self.ids_node != []:
                    for node_id in self.ids_node:
                        sql = "INSERT INTO " + self.schema_name + ".doc_x_node (doc_id, node_id )"
                        sql += " VALUES ('" + str(doc_id) + "', '" + str(node_id) + "')"
                        status = self.controller.execute_sql(sql)
                        if status:
                            message = "Values has been updated into table doc_x_node"
                            self.controller.show_info(message)
                        if not status:
                            message = "Error inserting element in table, you need to review data"
                            self.controller.show_warning(message)
                            return
                if self.ids_connec != []:
                    for connec_id in self.ids_connec:
                        sql = "INSERT INTO " + self.schema_name + ".doc_x_connec (doc_id, connec_id )"
                        sql += " VALUES ('" + str(doc_id) + "', '" + str(connec_id) + "')"
                        status = self.controller.execute_sql(sql)
                        if status:
                            message = "Values has been updated into table element_x_connec"
                            self.controller.show_info(message)
                        if not status:
                            message = "Error inserting element in table, you need to review data"
                            self.controller.show_warning(message)
                            return


        # If document doesn't exist perform an INSERT
        else:
            sql = "INSERT INTO " + self.schema_name + ".doc (id, doc_type, path, observ) "
            sql += " VALUES ('" + doc_id + "', '" + doc_type + "', '" + path + "', '" + observ +  "')"
            status = self.controller.execute_sql(sql)
            if status:
                message = "Values has been updated into table document"
                self.controller.show_info(message)

                if self.ids_arc != []:

                    for arc_id in self.ids_arc:
                        sql = "INSERT INTO " + self.schema_name + ".doc_x_arc (doc_id, arc_id )"
                        sql += " VALUES ('" + str(doc_id) + "', '" + str(arc_id) + "')"
                        status = self.controller.execute_sql(sql)
                        if status:
                            message = "Values has been updated into table doc_x_arc"
                            self.controller.show_info(message)
                        if not status:
                            message = "Error inserting element in table, you need to review data"
                            self.controller.show_warning(message)
                            return
                if self.ids_node != []:
                    for node_id in self.ids_node:
                        sql = "INSERT INTO " + self.schema_name + ".doc_x_node (doc_id, node_id )"
                        sql += " VALUES ('" + str(doc_id) + "', '" + str(node_id) + "')"
                        status = self.controller.execute_sql(sql)
                        if status:
                            message = "Values has been updated into table doc_x_node"
                            self.controller.show_info(message)
                        if not status:
                            message = "Error inserting element in table, you need to review data"
                            self.controller.show_warning(message)
                            return
                if self.ids_connec != []:
                    for connec_id in self.ids_connec:
                        sql = "INSERT INTO " + self.schema_name + ".doc_x_connec (doc_id, connec_id )"
                        sql += " VALUES ('" + str(doc_id) + "', '" + str(connec_id) + "')"
                        status = self.controller.execute_sql(sql)
                        if status:
                            message = "Values has been updated into table element_x_connec"
                            self.controller.show_info(message)
                        if not status:
                            message = "Error inserting element in table, you need to review data"
                            self.controller.show_warning(message)
                            return

            if not status:
                message = "Error inserting document in table, you need to review data"
                self.controller.show_warning(message, context_name='ui_message')
                return

        self.close_dialog()


    def add_point(self):
        """ Create the appropriate map tool and connect to the corresponding signal """
        map_canvas = self.iface.mapCanvas()
        self.emit_point = QgsMapToolEmitPoint(map_canvas)
        map_canvas.setMapTool(self.emit_point)
        self.emit_point.canvasClicked.connect(partial(self.get_xy))


    def get_xy(self, point):
        self.x = point.x()
        self.y = point.y()

        message = "Geometriy is added !"
        self.controller.show_info(message, context_name='ui_message')

        self.emit_point.canvasClicked.disconnect()


    def ed_add_el_autocomplete(self):
        """ Once we select 'element_id' using autocomplete, fill widgets with current values """

        self.dlg.element_id.setCompleter(self.completer)
        element_id = utils_giswater.getWidgetText("element_id")

        # Get values from database
        sql = "SELECT elementcat_id, location_type, ownercat_id, state, workcat_id,"
        sql += " buildercat_id, annotation, observ, comment, link, verified, rotation"
        sql += " FROM " + self.schema_name + ".element"
        sql += " WHERE element_id = '" + element_id + "'"
        row = self.dao.get_row(sql)

        # Fill widgets
        columns_length = self.dao.get_columns_length()
        for i in range(0, columns_length):
            column_name = self.dao.get_column_name(i)
            utils_giswater.setWidgetText(column_name, row[column_name])


    def ed_add_element_accept(self):
        """ Insert or update table 'element'. Add element to selected features """

        # Get values from dialog
        element_id = utils_giswater.getWidgetText("element_id")
        elementcat_id = utils_giswater.getWidgetText("elementcat_id")
        state = utils_giswater.getWidgetText("state")
        expl_id = utils_giswater.getWidgetText("expl_id")
        ownercat_id = utils_giswater.getWidgetText("ownercat_id")
        location_type = utils_giswater.getWidgetText("location_type")
        buildercat_id = utils_giswater.getWidgetText("buildercat_id")

        workcat_id = utils_giswater.getWidgetText("workcat_id")
        workcat_id_end = utils_giswater.getWidgetText("workcat_id_end")
        #annotation = utils_giswater.getWidgetText("annotation")
        comment = utils_giswater.getWidgetText("comment")
        observ = utils_giswater.getWidgetText("observ")
        link = utils_giswater.getWidgetText("path")
        verified = utils_giswater.getWidgetText("verified")
        rotation = utils_giswater.getWidgetText("rotation")

        builtdate = self.dlg.builtdate.dateTime().toString('yyyy-MM-dd')
        enddate = self.dlg.enddate.dateTime().toString('yyyy-MM-dd')

        undelete = self.dlg.undelete.isChecked()

        # TODO make join
        if state == 'OBSOLETE':
            state = '0'
        if state == 'ON SERVICE':
            state = '1'
        if state == 'PLANIFIED':
            state = '2'

        if expl_id == 'expl_01':
            expl_id = '1'
        if expl_id == 'expl_02':
            expl_id = '2'
        if expl_id == 'expl_03':
            expl_id = '3'
        if expl_id == 'expl_04':
            expl_id = '4'

        if element_id == 'null':
            # Show warning message
            message = "You need to insert element_id"
            self.controller.show_warning(message, context_name='ui_message')
            return

        # Get SRID
        srid = self.controller.plugin_settings_value('srid')   

        # Check if we already have data with selected element_id
        sql = "SELECT DISTINCT(element_id) FROM " + self.schema_name + ".element WHERE element_id = '" + str(element_id) + "'"
        row = self.dao.get_row(sql)
        
        # If element already exist perform an UPDATE
        if row:
            answer = self.controller.ask_question("Are you sure you want change the data?")
            if answer:
                sql = "UPDATE " + self.schema_name + ".element"
                sql += " SET elementcat_id = '" + str(elementcat_id) + "', state = '" + str(state) + "', location_type = '" + str(location_type) + "'"
                sql += ", workcat_id_end = '" + str(workcat_id_end) + "', workcat_id = '" + str(workcat_id) + "', buildercat_id = '" + str(buildercat_id) + "', ownercat_id = '" + str(ownercat_id) + "'"
                sql += ", rotation = '" + str(rotation) + "',comment = '" + str(comment) + "',expl_id = '" + str(expl_id) + "',observ = '" + str(observ) + "', link = '" + str(link) + "', verified = '" + str(verified) + "'"
                sql += ", undelete = '" + str(undelete) + "', enddate = '" + str(enddate) + "',builtdate = '" + str(builtdate) + "'"
                if str(self.x) != "":
                    sql += ", the_geom = ST_SetSRID(ST_MakePoint(" + str(self.x) + "," + str(self.y) + "), " + str(srid) + ")"
                else:
                    sql += ""
                sql += " WHERE element_id = '" + str(element_id) + "'"
                status = self.controller.execute_sql(sql)
                if status:
                    message = "Values has been updated into table element"
                    self.controller.show_info(message)

                    sql = "DELETE FROM " + self.schema_name + ".element_x_node WHERE  element_id = '" + str(element_id) + "'"
                    self.controller.execute_sql(sql)
                    sql = "DELETE FROM " + self.schema_name + ".element_x_arc WHERE  element_id = '" + str(element_id) + "'"
                    self.controller.execute_sql(sql)
                    sql = "DELETE FROM " + self.schema_name + ".element_x_connec WHERE  element_id = '" + str(element_id) + "'"
                    self.controller.execute_sql(sql)

                    if self.ids_arc != []:

                        for arc_id in self.ids_arc:
                            sql = "INSERT INTO " + self.schema_name + ".element_x_arc (element_id, arc_id )"
                            sql += " VALUES ('" + str(element_id) + "', '" + str(arc_id) + "')"
                            status = self.controller.execute_sql(sql)
                            if status:
                                message = "Values has been updated into table element_x_arc"
                                self.controller.show_info(message)
                            if not status:
                                message = "Error inserting element in table, you need to review data"
                                self.controller.show_warning(message)
                                return
                    if self.ids_node != []:
                        for node_id in self.ids_node:
                            sql = "INSERT INTO " + self.schema_name + ".element_x_node (element_id, node_id )"
                            sql += " VALUES ('" + str(element_id) + "', '" + str(node_id) + "')"
                            status = self.controller.execute_sql(sql)
                            if status:
                                message = "Values has been updated into table element_x_node"
                                self.controller.show_info(message)
                            if not status:
                                message = "Error inserting element in table, you need to review data"
                                self.controller.show_warning(message)
                                return
                    if self.ids_connec != []:
                        for connec_id in self.ids_connec:
                            sql = "INSERT INTO " + self.schema_name + ".element_x_connec (element_id, connec_id )"
                            sql += " VALUES ('" + str(element_id) + "', '" + str(connec_id) + "')"
                            status = self.controller.execute_sql(sql)
                            if status:
                                message = "Values has been updated into table element_x_connec"
                                self.controller.show_info(message)
                            if not status:
                                message = "Error inserting element in table, you need to review data"
                                self.controller.show_warning(message)
                                return

        # If element doesn't exist perform an INSERT
        else:
            sql = "INSERT INTO " + self.schema_name + ".element (element_id, elementcat_id, state, location_type"
            sql += ", workcat_id, buildercat_id, ownercat_id, rotation, comment, expl_id, observ, link, verified, workcat_id_end, enddate, builtdate, undelete"
            if str(self.x) != "":
                sql +=", the_geom) "
            else:
                sql += ")"
            sql += " VALUES ('" + str(element_id) + "', '" + str(elementcat_id) + "', '" + str(state) + "', '" + str(location_type) + "', '"
            sql += str(workcat_id) + "', '" + str(buildercat_id) + "', '" + str(ownercat_id) + "', '" + str(rotation) + "', '" + str(comment) + "', '"
            sql += str(expl_id) + "','" + str(observ) + "','" + str(link) + "','" + str(verified) + "','" + str(workcat_id_end) + "','" + str(enddate) + "','" + str(builtdate) + "','" + str(undelete) + "'"
            if str(self.x) != "" :
                sql += ",ST_SetSRID(ST_MakePoint(" + str(self.x) + "," + str(self.y) + "), " + str(srid) +"))"
            else:
                sql += ")"
            status = self.controller.execute_sql(sql)
            if status:
                message = "Values has been updated into table element"
                self.controller.show_info(message)

                if self.ids_arc != []:

                    for arc_id in self.ids_arc:
                        sql = "INSERT INTO " + self.schema_name + ".element_x_arc (element_id, arc_id )"
                        sql += " VALUES ('" + str(element_id) + "', '" + str(arc_id) + "')"
                        status = self.controller.execute_sql(sql)
                        if status:
                            message = "Values has been updated into table element element_x_arc"
                            self.controller.show_info(message)
                        if not status:
                            message = "Error inserting element in table, you need to review data"
                            self.controller.show_warning(message)
                            return
                if self.ids_node != []:
                    for node_id in self.ids_node:
                        sql = "INSERT INTO " + self.schema_name + ".element_x_node (element_id, node_id )"
                        sql += " VALUES ('" + str(element_id) + "', '" + str(node_id) + "')"
                        status = self.controller.execute_sql(sql)
                        if status:
                            message = "Values has been updated into table element element_x_node"
                            self.controller.show_info(message)
                        if not status:
                            message = "Error inserting element in table, you need to review data"
                            self.controller.show_warning(message)
                            return
                if self.ids_connec != []:
                    for connec_id in self.ids_connec:
                        sql = "INSERT INTO " + self.schema_name + ".element_x_connec (element_id, connec_id )"
                        sql += " VALUES ('" + str(element_id) + "', '" + str(connec_id) + "')"
                        status = self.controller.execute_sql(sql)
                        if status:
                            message = "Values has been updated into table element_x_connec"
                            self.controller.show_info(message)
                        if not status:
                            message = "Error inserting element in table, you need to review data"
                            self.controller.show_warning(message)
                            return
            if not status:
                message = "Error inserting element in table, you need to review data"
                self.controller.show_warning(message)
                return

        self.close_dialog(self.dlg)
        self.iface.mapCanvas().refreshAllLayers()


    def ed_add_to_feature(self, table_name, value_id):
        """ Add document or element to selected features """

        # Get schema and table name of selected layer
        layer_source = self.controller.get_layer_source(self.layer)
        uri_table = layer_source['table']
        if uri_table is None:
            msg = "Error getting table name from selected layer"
            self.controller.show_warning(msg, context_name='ui_message')
            return

        elem_type = None
        field_id = None

        if self.table_arc in uri_table:
            elem_type = "arc"
            field_id = "arc_id"
        if self.table_node in uri_table:
            elem_type = "node"
            field_id = "node_id"
        if self.table_connec in uri_table:
            elem_type = "connec"
            field_id = "connec_id"
        if self.table_gully in uri_table:
            elem_type = "gully"
            field_id = "gully_id"

        if self.table_man_arc in uri_table:
            elem_type = "arc"
            field_id = "arc_id"
        if self.table_man_node in uri_table:
            elem_type = "node"
            field_id = "node_id"
        if self.table_man_connec in uri_table:
            elem_type = "connec"
            field_id = "connec_id"
        if self.table_man_gully in uri_table:
            elem_type = "gully"
            field_id = "gully_id"

        if self.table_wjoin in uri_table:
            elem_type = "connec"
            field_id = "connec_id"
        if self.table_tap in uri_table:
            elem_type = "connec"
            field_id = "connec_id"
        if self.table_greentap in uri_table:
            elem_type = "connec"
            field_id = "connec_id"
        if self.table_fountain in uri_table:
            elem_type = "connec"
            field_id = "connec_id"

        if self.table_tank in uri_table:
            elem_type = "node"
            field_id = "node_id"
        if self.table_pump in uri_table:
            elem_type = "node"
            field_id = "node_id"
        if self.table_source in uri_table:
            elem_type = "node"
            field_id = "node_id"
        if self.table_meter in uri_table:
            elem_type = "node"
            field_id = "node_id"
        if self.table_junction in uri_table:
            elem_type = "node"
            field_id = "node_id"
        if self.table_waterwell in uri_table:
            elem_type = "node"
            field_id = "node_id"
        if self.table_reduction in uri_table:
            elem_type = "node"
            field_id = "node_id"
        if self.table_hydrant in uri_table:
            elem_type = "node"
            field_id = "node_id"
        if self.table_valve in uri_table:
            elem_type = "node"
            field_id = "node_id"
        if self.table_manhole in uri_table:
            elem_type = "node"
            field_id = "node_id"

        if self.table_chamber in uri_table:
            elem_type = "node"
            field_id = "node_id"
        if self.table_chamber_pol in uri_table:
            elem_type = "node"
            field_id = "node_id"
        if self.table_netgully in uri_table:
            elem_type = "node"
            field_id = "node_id"
        if self.table_netgully_pol in uri_table:
            elem_type = "node"
            field_id = "node_id"
        if self.table_netinit in uri_table:
            elem_type = "node"
            field_id = "node_id"
        if self.table_wjump in uri_table:
            elem_type = "node"
            field_id = "node_id"
        if self.table_wwtp in uri_table:
            elem_type = "node"
            field_id = "node_id"
        if self.table_wwtp_pol in uri_table:
            elem_type = "node"
            field_id = "node_id"
        if self.table_storage in uri_table:
            elem_type = "node"
            field_id = "node_id"
        if self.table_storage_pol in uri_table:
            elem_type = "node"
            field_id = "node_id"
        if self.table_outfall in uri_table:
            elem_type = "node"
            field_id = "node_id"

        if self.table_varc in uri_table:
            elem_type = "arc"
            field_id = "arc_id"
        if self.table_siphon in uri_table:
            elem_type = "arc"
            field_id = "arc_id"
        if self.table_conduit in uri_table:
            elem_type = "arc"
            field_id = "arc_id"
        if self.table_waccel in uri_table:
            elem_type = "arc"
            field_id = "arc_id"
        if 'v_edit_man_pipe' in uri_table:
            elem_type = "arc"
            field_id = "arc_id"

        if field_id is None:
            self.controller.show_info("Current active layer is different than selected features")
            return

        # Get selected features
        features = self.layer.selectedFeatures()
        for feature in features:
            elem_id = feature.attribute(field_id)

            sql = "SELECT * FROM " + self.schema_name + "." + table_name + "_x_" + elem_type
            sql += " WHERE " + field_id + " = '" + elem_id + "' AND " + value_id + " = " + table_name + "_id"
            row = self.dao.get_row(sql)
            if row is None:
                sql = "INSERT INTO " + self.schema_name + "." + table_name + "_x_" + elem_type + " (" + field_id + ", " + table_name + "_id) "
                sql += " VALUES ('" + elem_id + "', '" + value_id + "')"
                self.controller.execute_sql(sql)


    def edit_check(self):
        """ Initial check for buttons 33 and 34 """

        # Uncheck all actions (buttons) except this one
        self.controller.check_actions(False)
        self.controller.check_action(True, 32)

        # Check if at least one node is checked
        self.layer = self.iface.activeLayer()
        if self.layer is None:
            message = "You have to select a layer"
            self.controller.show_info(message, context_name='ui_message')
            return False

        count = self.layer.selectedFeatureCount()
        if count == 0:
            message = "You have to select at least one feature!"
            self.controller.show_info(message, context_name='ui_message')
            return False

        return True


    def edit_config_edit(self):
        """ Button 98: Open a dialog showing data from table 'config_param_user' """

        # Create the dialog and signals
        self.dlg = ConfigEdit()
        utils_giswater.setDialog(self.dlg)
        self.load_settings(self.dlg)
        self.dlg.btn_accept.pressed.connect(self.edit_config_edit_accept)
        self.dlg.btn_cancel.pressed.connect(partial(self.close_dialog, self.dlg))
        self.dlg.rejected.connect(partial(self.save_settings, self.dlg))
        
        # Set values from widgets of type QComboBox and dates
        # QComboBox Utils
        sql = "SELECT DISTINCT(name) FROM " + self.schema_name + ".value_state ORDER BY name"
        rows = self.dao.get_rows(sql)
        utils_giswater.fillComboBox("state_vdefault", rows)
        sql = "SELECT DISTINCT(id) FROM " + self.schema_name + ".cat_work ORDER BY id"
        rows = self.dao.get_rows(sql)
        utils_giswater.fillComboBox("workcat_vdefault", rows)
        sql = "SELECT DISTINCT(id) FROM " + self.schema_name + ".value_verified ORDER BY id"
        rows = self.dao.get_rows(sql)
        utils_giswater.fillComboBox("verified_vdefault", rows)

        sql = 'SELECT value FROM ' + self.schema_name + '.config_param_user'
        sql += ' WHERE "cur_user" = current_user AND parameter = ' + "'builtdate_vdefault'"
        row = self.dao.get_row(sql)
        if row is not None:
            date_value = datetime.strptime(row[0], '%Y-%m-%d')
        else:
            date_value = QDate.currentDate()
        utils_giswater.setCalendarDate("builtdate_vdefault", date_value)

        sql = "SELECT DISTINCT(id) FROM " + self.schema_name + ".cat_arc ORDER BY id"
        rows = self.dao.get_rows(sql)
        utils_giswater.fillComboBox("arccat_vdefault", rows)
        sql = "SELECT DISTINCT(id) FROM " + self.schema_name + ".cat_node ORDER BY id"
        rows = self.dao.get_rows(sql)
        utils_giswater.fillComboBox("nodecat_vdefault", rows)
        sql = "SELECT DISTINCT(id) FROM " + self.schema_name + ".cat_connec ORDER BY id"
        rows = self.dao.get_rows(sql)
        utils_giswater.fillComboBox("connecat_vdefault", rows)

        # QComboBox Ud
        sql = "SELECT DISTINCT(id) FROM " + self.schema_name + ".node_type ORDER BY id"
        rows = self.dao.get_rows(sql)
        utils_giswater.fillComboBox("nodetype_vdefault", rows)
        sql = "SELECT DISTINCT(id) FROM " + self.schema_name + ".arc_type ORDER BY id"
        rows = self.dao.get_rows(sql)
        utils_giswater.fillComboBox("arctype_vdefault", rows)
        sql = "SELECT DISTINCT(id) FROM " + self.schema_name + ".connec_type ORDER BY id"
        rows = self.dao.get_rows(sql)
        utils_giswater.fillComboBox("connectype_vdefault", rows)

        sql = "SELECT parameter, value FROM " + self.schema_name + ".config_param_user"
        rows = self.dao.get_rows(sql)
        for row in rows:
            utils_giswater.setWidgetText(str(row[0]), str(row[1]))
            utils_giswater.setChecked("chk_" + str(row[0]), True)

        sql = "SELECT name FROM " + self.schema_name + ".value_state WHERE id::text = "
        sql += "(SELECT value FROM " + self.schema_name + ".config_param_user WHERE parameter = 'state_vdefault')::text"
        rows = self.dao.get_rows(sql)
        if rows:
            utils_giswater.setWidgetText("state_vdefault", str(rows[0][0]))

        if self.project_type == 'ws':
            self.dlg.tab_config.removeTab(1)
            self.dlg.tab_config.removeTab(1)
        elif self.project_type == 'ud':
            self.dlg.tab_config.removeTab(1)

        self.dlg.exec_()


    def edit_config_edit_accept(self):

        if utils_giswater.isChecked("chk_state_vdefault"):
            self.insert_or_update_config_param_curuser(self.dlg.state_vdefault, "state_vdefault", "config_param_user")
        else:
            self.delete_row("state_vdefault", "config_param_user")
        if utils_giswater.isChecked("chk_workcat_vdefault"):
            self.insert_or_update_config_param_curuser(self.dlg.workcat_vdefault, "workcat_vdefault", "config_param_user")
        else:
            self.delete_row("workcat_vdefault", "config_param_user")
        if utils_giswater.isChecked("chk_verified_vdefault"):
            self.insert_or_update_config_param_curuser(self.dlg.verified_vdefault, "verified_vdefault", "config_param_user")
        else:
            self.delete_row("verified_vdefault", "config_param_user")
        if utils_giswater.isChecked("chk_builtdate_vdefault"):
            self.insert_or_update_config_param_curuser(self.dlg.builtdate_vdefault, "builtdate_vdefault", "config_param_user")
        else:
            self.delete_row("builtdate_vdefault", "config_param_user")
        if utils_giswater.isChecked("chk_arccat_vdefault"):
            self.insert_or_update_config_param_curuser(self.dlg.arccat_vdefault, "arccat_vdefault", "config_param_user")
        else:
            self.delete_row("arccat_vdefault", "config_param_user")
        if utils_giswater.isChecked("chk_nodecat_vdefault"):
            self.insert_or_update_config_param_curuser(self.dlg.nodecat_vdefault, "nodecat_vdefault", "config_param_user")
        else:
            self.delete_row("nodecat_vdefault", "config_param_user")
        if utils_giswater.isChecked("chk_connecat_vdefault"):
            self.insert_or_update_config_param_curuser(self.dlg.connecat_vdefault, "connecat_vdefault", "config_param_user")
        else:
            self.delete_row("connecat_vdefault", "config_param_user")
        if utils_giswater.isChecked("chk_nodetype_vdefault"):
            self.insert_or_update_config_param_curuser(self.dlg.nodetype_vdefault, "nodetype_vdefault", "config_param_user")
        else:
            self.delete_row("nodetype_vdefault", "config_param_user")
        if utils_giswater.isChecked("chk_arctype_vdefault"):
            self.insert_or_update_config_param_curuser(self.dlg.arctype_vdefault, "arctype_vdefault", "config_param_user")
        else:
            self.delete_row("arctype_vdefault", "config_param_user")
        if utils_giswater.isChecked("chk_connectype_vdefault"):
            self.insert_or_update_config_param_curuser(self.dlg.connectype_vdefault, "connectype_vdefault", "config_param_user")
        else:
            self.delete_row("connectype_vdefault", "config_param_user")

        message = "Values has been updated"
        self.controller.show_info(message, context_name='ui_message')
        self.close_dialog(self.dlg)


    def insert_or_update_config_param_curuser(self, widget, parameter, tablename):
        """ Insert or update values in tables with current_user control """

        sql = 'SELECT * FROM ' + self.schema_name + '.' + tablename + ' WHERE "cur_user" = current_user'
        rows = self.controller.get_rows(sql)
        exist_param = False
        if type(widget) != QDateEdit:
            if widget.currentText() != "":
                for row in rows:
                    if row[1] == parameter:
                        exist_param = True
                if exist_param:
                    sql = "UPDATE " + self.schema_name + "." + tablename + " SET value="
                    if widget.objectName() != 'state_vdefault':
                        sql += "'" + widget.currentText() + "' WHERE parameter='" + parameter + "'"
                    else:
                        sql += "(SELECT id FROM " + self.schema_name + ".value_state WHERE name ='" + widget.currentText() + "')"
                        sql += " WHERE parameter = 'state_vdefault' "
                else:
                    sql = 'INSERT INTO ' + self.schema_name + '.' + tablename + '(parameter, value, cur_user)'
                    if widget.objectName() != 'state_vdefault':
                        sql += " VALUES ('" + parameter + "', '" + widget.currentText() + "', current_user)"
                    else:
                        sql += " VALUES ('" + parameter + "', (SELECT id FROM " + self.schema_name + ".value_state WHERE name ='" + widget.currentText() + "'), current_user)"
        else:
            for row in rows:
                if row[1] == parameter:
                    exist_param = True
            if exist_param:
                sql = "UPDATE " + self.schema_name + "." + tablename + " SET value="
                _date = widget.dateTime().toString('yyyy-MM-dd')
                sql += "'" + str(_date) + "' WHERE parameter='" + parameter + "'"
            else:
                sql = 'INSERT INTO ' + self.schema_name + '.' + tablename + '(parameter, value, cur_user)'
                _date = widget.dateTime().toString('yyyy-MM-dd')
                sql += " VALUES ('" + parameter + "', '" + _date + "', current_user)"

        self.controller.execute_sql(sql)


    def delete_row(self,  parameter, tablename):
        sql = 'DELETE FROM ' + self.schema_name + '.' + tablename
        sql += ' WHERE "cur_user" = current_user AND parameter = ' + "'" + parameter + "'"
        self.controller.execute_sql(sql)


    def populate_combo(self, widget, table_name, field_name="id"):
        """ Executes query and fill combo box """

        sql = "SELECT " + field_name
        sql += " FROM " + self.schema_name + "." + table_name + " ORDER BY " + field_name
        rows = self.dao.get_rows(sql)
        utils_giswater.fillComboBox(widget, rows)
        if len(rows) > 0:
            utils_giswater.setCurrentIndex(widget, 0)


    def edit_dimensions(self):
        """ Button 39: Dimensioning """

        layer = QgsMapLayerRegistry.instance().mapLayersByName("Dimensioning")
        if layer:
            layer = layer[0]
            self.iface.setActiveLayer(layer)
            layer.startEditing()
            # Implement the Add Feature button
            self.iface.actionAddFeature().trigger()
        else:
            message = "Layer name not found"
            self.controller.show_warning(message, parameter="Dimensioning")
        


    def edit_add_visit(self):
        ''' Btn_64 : add visit '''

        # Create the dialog and signals
        self.dlg_visit = AddVisit()
        utils_giswater.setDialog(self.dlg_visit)

        # Show future id of visit
        sql = "SELECT MAX(id) FROM " + self.schema_name + ".om_visit "
        row = self.controller.get_row(sql)
        if row:
            visit_id = row[0] + 1
            self.dlg_visit.visit_id.setText(str(visit_id))

        # Set icons
        self.set_icon(self.dlg_visit.add_geom, "133")
        self.set_icon(self.dlg_visit.btn_insert_event, "111")
        self.set_icon(self.dlg_visit.btn_delete_event, "112")
        self.set_icon(self.dlg_visit.btn_open_event, "140")
        self.set_icon(self.dlg_visit.btn_open_gallery, "136")

        self.set_icon(self.dlg_visit.btn_insert, "111")
        self.set_icon(self.dlg_visit.btn_delete, "112")
        self.set_icon(self.dlg_visit.btn_snapping, "137")

        # Set icons tab document
        self.set_icon(self.dlg_visit.btn_doc_insert, "111")
        self.set_icon(self.dlg_visit.btn_doc_delete, "112")
        self.set_icon(self.dlg_visit.btn_doc_new, "134")
        self.set_icon(self.dlg_visit.btn_open_doc, "170")


        #self.set_icon(self.dlg_visit.btn_open, "140")

        # Set widgets
        self.visit_id = self.dlg_visit.findChild(QLineEdit, "visit_id")
        self.ext_code = self.dlg_visit.findChild(QLineEdit, "ext_code")
        self.descript = self.dlg_visit.findChild(QLineEdit, "descript")

        self.visitcat_id = self.dlg_visit.findChild(QComboBox, "visitcat_id")
        self.startdate = self.dlg_visit.findChild(QDateTimeEdit, "startdate")
        self.enddate = self.dlg_visit.findChild(QDateTimeEdit, "enddate")
        self.expl_id = self.dlg_visit.findChild(QComboBox, "expl_id")
        self.uncertain = self.dlg_visit.findChild(QCheckBox, "uncertain")

        self.btn_accept = self.dlg_visit.findChild(QPushButton ,"btn_accept")
        self.btn_cancel = self.dlg_visit.findChild(QPushButton ,"btn_cancel")

        self.event_id = self.dlg_visit.findChild(QLineEdit, "event_id")
        self.btn_add_geom = self.dlg_visit.findChild(QPushButton ,"add_geom")
        self.btn_add_geom.pressed.connect(self.add_point)
        self.btn_insert_event = self.dlg_visit.findChild(QPushButton ,"btn_insert_event")
        self.btn_insert_event.pressed.connect(self.insert_event)
        self.btn_delete_event = self.dlg_visit.findChild(QPushButton ,"btn_delete_event")
        self.btn_delete_event.pressed.connect(self.delete_event)
        self.btn_open_gallery = self.dlg_visit.findChild(QPushButton ,"btn_open_gallery")
        self.btn_open_gallery.pressed.connect(self.open_gallery)
        self.btn_open_event = self.dlg_visit.findChild(QPushButton ,"btn_open_event")
        self.btn_open_event.pressed.connect(self.open_event)
        self.tbl_event = self.dlg_visit.findChild(QTableView ,"tbl_event")

        # Set widgets of tab document
        self.date_document_from = self.dlg_visit.findChild(QDateEdit, "date_document_from")
        self.date_document_to = self.dlg_visit.findChild(QDateEdit, "date_document_to")
        self.doc_type = self.dlg_visit.findChild(QComboBox, "doc_type")
        self.doc_id = self.dlg_visit.findChild(QLineEdit, "doc_id")
        self.btn_doc_insert = self.dlg_visit.findChild(QPushButton ,"btn_doc_insert")
        self.btn_doc_insert.pressed.connect(self.insert_document)
        self.btn_doc_delete = self.dlg_visit.findChild(QPushButton ,"btn_doc_delete")
        self.btn_doc_delete.pressed.connect(self.delete_document)
        self.btn_doc_new = self.dlg_visit.findChild(QPushButton ,"btn_doc_new")
        self.btn_doc_new.pressed.connect(self.add_new_doc)
        self.btn_open_doc = self.dlg_visit.findChild(QPushButton ,"btn_open_doc")
        self.btn_open_doc.pressed.connect(self.open_document)
        self.tbl_document = self.dlg_visit.findChild(QTableView ,"tbl_document")

        # Set signals
        self.doc_type.activated.connect(self.set_filter_document)
        self.date_document_to.dateChanged.connect(self.set_filter_document)
        self.date_document_from.dateChanged.connect(self.set_filter_document)

        # Adding auto-completion to a QLineEdit - visit_id
        self.completer = QCompleter()
        self.dlg_visit.visit_id.setCompleter(self.completer)
        model = QStringListModel()

        sql = "SELECT DISTINCT(id) FROM " + self.schema_name + ".om_visit"
        rows = self.controller.get_rows(sql)
        values = []
        for row in rows:
            values.append(str(row[0]))

        model.setStringList(values)
        self.completer.setModel(model)

        self.dlg_visit.visit_id.textChanged.connect(self.check_visit_exist)

        # Adding auto-completion to a QLineEdit - event_id
        self.completer = QCompleter()
        self.event_id.setCompleter(self.completer)
        model = QStringListModel()

        sql = "SELECT DISTINCT(id) FROM " + self.schema_name + ".om_visit_parameter"
        rows = self.controller.get_rows(sql)
        values = []
        for row in rows:
            values.append(str(row[0]))

        model.setStringList(values)
        self.completer.setModel(model)



        # Fill ComboBox visitcat_id
        sql = "SELECT name"
        sql += " FROM " + self.schema_name + ".om_visit_cat"
        sql += " ORDER BY name"
        rows = self.controller.get_rows(sql)
        if rows != []:
            utils_giswater.fillComboBox("visitcat_id", rows)

        # Fill ComboBox expl_id
        sql = "SELECT name"
        sql += " FROM " + self.schema_name + ".exploitation"
        sql += " ORDER BY name"
        rows = self.controller.get_rows(sql)
        if rows != []:
            utils_giswater.fillComboBox("expl_id", rows)

        # Fill ComboBox doccat_id
        sql = "SELECT DISTINCT(doc_type)"
        sql += " FROM " + self.schema_name +".v_ui_doc_x_node"
        sql += " ORDER BY doc_type"
        rows = self.controller.get_rows(sql)
        if rows != []:
            utils_giswater.fillComboBox("doc_type", rows)


        # Adding auto-completion to a QLineEdit - event_id
        self.completer = QCompleter()
        self.dlg_visit.event_id.setCompleter(self.completer)
        model = QStringListModel()

        sql = "SELECT DISTINCT(id) FROM " + self.schema_name + ".om_visit_parameter"
        rows = self.controller.get_rows(sql)
        values = []
        for row in rows:
            values.append(str(row[0]))

        model.setStringList(values)
        self.completer.setModel(model)


        # Adding auto-completion to a QLineEdit - document_id
        self.completer = QCompleter()
        self.dlg_visit.doc_id.setCompleter(self.completer)
        model = QStringListModel()

        sql = "SELECT DISTINCT(id) FROM " + self.schema_name + ".doc"
        rows = self.controller.get_rows(sql)
        values = []
        for row in rows:
            values.append(str(row[0]))

        model.setStringList(values)
        self.completer.setModel(model)


        # Open the dialog
        self.dlg_visit.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.dlg_visit.open()


    def set_filter_document(self):
        """ Get values selected by the user and sets a new filter for its table model """

        # Get selected dates
        date_from = self.date_document_from.date().toString('yyyyMMdd')
        date_to = self.date_document_to.date().toString('yyyyMMdd')
        if (date_from > date_to):
            message = "Selected date interval is not valid"
            self.controller.show_warning(message)
            return

        # Set filter
        expr = " date >= '" + str(date_from) + "' AND date <= '" + str(date_to) + "'"

        # Get selected values in Comboboxes
        doc_type_value = utils_giswater.getWidgetText("doc_type")


        if str(doc_type_value) != 'null':
            expr += " AND doc_type = '" + str(doc_type_value) + "'"

        # Refresh model with selected filter
        self.tbl_document.model().setFilter(expr)
        self.tbl_document.model().select()


    def fill_table_visit(self, widget, table_name, filter_):
        ''' Set a model with selected filter.
        Attach that model to selected table
        '''

        # Set model
        model = QSqlTableModel();
        model.setTable(table_name)
        model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        model.setFilter(filter_)
        model.select()

        # Check for errors
        if model.lastError().isValid():
            self.controller.show_warning(model.lastError().text())

        # Attach model to table view
        widget.setModel(model)
        widget.show()


    def check_visit_exist(self):

        # Tab event
        # Check if we already have data with selected visit_id
        visit_id = self.dlg_visit.visit_id.text()
        sql = "SELECT DISTINCT(id) FROM " + self.schema_name + ".om_visit WHERE id = '" + str(visit_id) + "'"
        row = self.dao.get_row(sql)
        if row:
            # If element exist : load data ELEMENT
            sql = "SELECT * FROM " + self.schema_name + ".om_visit WHERE id = '" + str(visit_id) + "'"
            row = self.dao.get_row(sql)

            # Set data
            self.dlg_visit.ext_code.setText(str(row['ext_code']))

            # TODO join
            if str(row['visitcat_id']) == '1':
                visitcat_id = "Test"

            utils_giswater.setWidgetText("visitcat_id", str(visitcat_id))

            self.dlg_visit.descript.setText(str(row['descript']))


            # Fill table event depending of visit_id
            visit_id = self.visit_id.text()
            self.filter = "visit_id = '" + str(visit_id) + "'"
            self.fill_table_visit(self.tbl_event, self.schema_name+".om_visit_event", self.filter)

            # Tab document
            self.fill_table_visit(self.tbl_document, self.schema_name + ".v_ui_doc_x_visit", self.filter)


    def insert_event(self):

        event_id = self.dlg_visit.event_id.text()
        if event_id != '':
            sql = "SELECT form_type FROM " + self.schema_name + ".om_visit_parameter WHERE id = '" + str(event_id) + "'"
            row = self.dao.get_row(sql)
            form_type = str(row[0])
        else:
            message = "You need to enter id"
            self.controller.show_info_box(message)
            return

        if form_type == 'event_ud_arc_standard':
            self.dlg_event = EventUDarcStandard()
        if form_type == 'event_ud_arc_rehabit':
            self.dlg_event = EventUDarcRehabit()
        if form_type == 'event_standard':
            self.dlg_event = EventStandard()

        utils_giswater.setDialog(self.dlg_event)

        self.dlg_event.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.dlg_event.exec_()


    def open_event(self):

        # Get selected rows
        selected_list = self.dlg_visit.tbl_event.selectionModel().selectedRows()
        if len(selected_list) == 0:
            message = "Any record selected"
            self.controller.show_info_box(message)
            return
        elif len(selected_list) > 1:
            message = "More then one event selected. Select just one event."
            self.controller.show_warning(message)
            return
        else:
            row = selected_list[0].row()
            parameter_id = self.dlg_visit.tbl_event.model().record(row).value("parameter_id")
            event_id = self.dlg_visit.tbl_event.model().record(row).value("id")

            sql = "SELECT form_type FROM " + self.schema_name + ".om_visit_parameter WHERE id = '" + str(parameter_id) + "'"
            row = self.dao.get_row(sql)
            form_type = str(row[0])

            sql = "SELECT * FROM " + self.schema_name + ".om_visit_event WHERE id = '" + str(event_id) + "'"
            row = self.dao.get_row(sql)

            if form_type == 'event_ud_arc_standard':
                self.dlg_event = EventUDarcStandard()
                # Force fill data
                # TODO set parameter id
                #self.dlg_event.parameter_id

                self.dlg_event.value.setText(str(row['value']))
                self.dlg_event.position_id.setText(str(row['position_id']))
                self.dlg_event.position_value.setText(str(row['position_value']))
                self.dlg_event.text.setText(str(row['text']))

            if form_type == 'event_ud_arc_rehabit':

                self.dlg_event = EventUDarcRehabit()
                # Force fill data
                # self.dlg_event.parameter_id

                self.dlg_event.position_id.setText(str(row['position_id']))
                self.dlg_event.position_value.setText(str(row['position_value']))
                self.dlg_event.text.setText(str(row['text']))
                self.dlg_event.value1.setText(str(row['value1']))
                self.dlg_event.value2.setText(str(row['value2']))
                self.dlg_event.geom1.setText(str(row['geom1']))
                self.dlg_event.geom2.setText(str(row['geom2']))
                self.dlg_event.geom3.setText(str(row['geom3']))


            if form_type == 'event_standard':
                self.dlg_event = EventStandard()
                # Force fill data
                # self.dlg_event.parameter_id

                self.dlg_event.value.setText(str(row['value']))
                self.dlg_event.text.setText(str(row['text']))


            utils_giswater.setDialog(self.dlg_event)

            self.dlg_event.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.dlg_event.exec_()



    def delete_event(self):

        # Get selected rows
        selected_list = self.dlg_visit.tbl_event.selectionModel().selectedRows()
        if len(selected_list) == 0:
            message = "Any record selected"
            self.controller.show_info_box(message)
            return
        selected_id = []
        inf_text = ""
        list_id = ""
        for i in range(0, len(selected_list)):
            row = selected_list[i].row()
            event_id = self.dlg_visit.tbl_event.model().record(row).value("id")
            selected_id.append(str(event_id))
            inf_text += str(event_id) + ", "
            list_id = list_id + "'" + str(event_id) + "', "
        inf_text = inf_text[:-2]
        list_id = list_id[:-2]
        answer = self.controller.ask_question("Are you sure you want to delete these records?", "Delete records",
                                              inf_text)
        if answer:
            for el in selected_id:
                sql = "DELETE FROM "+self.schema_name+".om_visit_event"
                sql += " WHERE id = '" +str(el)+"'"
                status = self.controller.execute_sql(sql)
                if not status:
                    message = "Error deliting data"
                    self.controller.show_warning(message)
                    return
                elif status:
                    message = "Event deleted"
                    self.controller.show_info(message)

                    self.dlg_visit.tbl_event.model().select()



    def open_document(self):

        # Get selected rows
        selected_list = self.dlg_visit.tbl_document.selectionModel().selectedRows()
        if len(selected_list) == 0:
            message = "Any record selected"
            self.controller.show_info_box(message)
            return
        elif len(selected_list) > 1:
            message = "More then one document selected. Select just one document."
            self.controller.show_warning(message)
            return
        else:
            row = selected_list[0].row()
            path = self.dlg_visit.tbl_document.model().record(row).value('path')
            # Check if file exist
            if not os.path.exists(path):
                message = "File not found!"
                self.controller.show_warning(message)
            else:
                # Open the document
                os.startfile(path)


    def delete_document(self):

        # Get selected rows
        selected_list = self.dlg_visit.tbl_document.selectionModel().selectedRows()
        if len(selected_list) == 0:
            message = "Any record selected"
            self.controller.show_info_box(message)
            return
        selected_id = []
        inf_text = ""
        list_id = ""
        for i in range(0, len(selected_list)):
            row = selected_list[i].row()
            doc_id = self.dlg_visit.tbl_document.model().record(row).value("id")
            selected_id.append(str(doc_id))
            inf_text += str(doc_id) + ", "
            list_id = list_id + "'" + str(doc_id) + "', "
        inf_text = inf_text[:-2]
        list_id = list_id[:-2]
        answer = self.controller.ask_question("Are you sure you want to delete these records?", "Delete records",
                                              inf_text)
        if answer:
            for el in selected_id:
                sql = "DELETE FROM " + self.schema_name + ".doc_x_visit"
                sql += " WHERE id = '" + str(el) + "'"
                status = self.controller.execute_sql(sql)
                if not status:
                    message = "Error deliting data"
                    self.controller.show_warning(message)
                    return
                elif status:
                    message = "Event deleted"
                    self.controller.show_info(message)

                    self.dlg_visit.tbl_document.model().select()


    def add_new_doc(self):

        # Call function of button add_doc
        self.edit_add_file()


    def open_gallery(self):

        # Get absolute path
        sql = "SELECT value FROM " + self.schema_name + ".config_param_system"
        sql += " WHERE parameter = 'doc_absolute_path'"
        row = self.dao.get_row(sql)
        absolute_path = str(row[0])

        # Get selected rows
        selected_list = self.dlg_visit.tbl_event.selectionModel().selectedRows()
        if len(selected_list) == 0:
            message = "Any record selected"
            self.controller.show_info_box(message)
            return
        elif len(selected_list) > 1:
            message = "More then one document selected. Select just one document."
            self.controller.show_warning(message)
            return
        else:
            row = selected_list[0].row()
            relative_path = self.dlg_visit.tbl_event.model().record(row).value('value')
            path = str(absolute_path + relative_path)
            # Check if file exist
            if not os.path.exists(path):
                message = "File not found!"
                self.controller.show_warning(message)
            else:
                # Open the document
                os.startfile(path)


    def insert_document(self):

        #self TODO if document new
        doc_id = self.doc_id.text()
        visit_id = self.visit_id.text()
        if doc_id == 'null':
            # Show warning message
            message = "You need to insert doc_id"
            self.controller.show_warning(message, context_name='ui_message')
            return

        if visit_id == 'null':
            # Show warning message
            message = "You need to insert visit_id"
            self.controller.show_warning(message, context_name='ui_message')
            return

        # Insert into new table
        sql = "INSERT INTO " + self.schema_name + ".doc_x_visit (doc_id, visit_id)"
        sql += " VALUES (" + str(doc_id) + "," + str(visit_id) + ")"
        status = self.controller.execute_sql(sql)
        if status:
            message = "Document inserted successfully"
            self.controller.show_info(message)

        self.dlg_visit.tbl_document.model().select()




