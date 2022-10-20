import os
import sys
from click.testing import CliRunner
from swsscommon.swsscommon import SonicV2Connector
from utilities_common.db import Db

import config.main as config
import show.main as show

test_path = os.path.dirname(os.path.abspath(__file__))
mock_db_path = os.path.join(test_path, "vrf_input")

class TestShowVrf(object):
    @classmethod
    def setup_class(cls):
        print("SETUP")
        os.environ["UTILITIES_UNIT_TESTING"] = "1"

    def test_vrf_show(self):
        from .mock_tables import dbconnector
        jsonfile_config = os.path.join(mock_db_path, "config_db")
        dbconnector.dedicated_dbs['CONFIG_DB'] = jsonfile_config
        runner = CliRunner()
        db = Db()
        expected_output = """\
VRF     Interfaces
------  ---------------
Vrf1
Vrf101  Ethernet0.10
Vrf102  PortChannel0002
        Vlan40
        Eth32.10
Vrf103  Ethernet4
        Loopback0
        Po0002.101
"""
       
        result = runner.invoke(show.cli.commands['vrf'], [], obj=db)
        dbconnector.dedicated_dbs = {}
        assert result.exit_code == 0
        assert result.output == expected_output

    def test_vrf_bind_unbind(self):
        from .mock_tables import dbconnector
        jsonfile_config = os.path.join(mock_db_path, "config_db")
        dbconnector.dedicated_dbs['CONFIG_DB'] = jsonfile_config
        runner = CliRunner()
        db = Db()
        expected_output = """\
VRF     Interfaces
------  ---------------
Vrf1
Vrf101  Ethernet0.10
Vrf102  PortChannel0002
        Vlan40
        Eth32.10
Vrf103  Ethernet4
        Loopback0
        Po0002.101
"""
       
        result = runner.invoke(show.cli.commands['vrf'], [], obj=db)
        dbconnector.dedicated_dbs = {}
        assert result.exit_code == 0
        assert result.output == expected_output

        obj = {'config_db':db.cfgdb}

        expected_output_unbind = "Interface Ethernet4 IPv4 disabled and address(es) removed due to unbinding VRF."
        result = runner.invoke(config.config.commands["interface"].commands["vrf"].commands["unbind"], ["Ethernet4"], obj=obj)
        print(result.exit_code, result.output)
        assert result.exit_code == 0
        assert 'Ethernet4' not in db.cfgdb.get_table('INTERFACE')
        assert result.output == expected_output_unbind
        
        expected_output_unbind = "Interface Loopback0 IPv4 disabled and address(es) removed due to unbinding VRF."
        result = runner.invoke(config.config.commands["interface"].commands["vrf"].commands["unbind"], ["Loopback0"], obj=obj)
        print(result.exit_code, result.output)
        assert result.exit_code == 0
        assert 'Loopback0' not in db.cfgdb.get_table('LOOPBACK_INTERFACE')
        assert result.output == expected_output_unbind

        expected_output_unbind = "Interface Vlan40 IPv4 disabled and address(es) removed due to unbinding VRF."
        result = runner.invoke(config.config.commands["interface"].commands["vrf"].commands["unbind"], ["Vlan40"], obj=obj)
        print(result.exit_code, result.output)
        assert result.exit_code == 0
        assert 'Vlan40' not in db.cfgdb.get_table('VLAN_INTERFACE')
        assert result.output == expected_output_unbind

        expected_output_unbind = "Interface PortChannel0002 IPv4 disabled and address(es) removed due to unbinding VRF."
        result = runner.invoke(config.config.commands["interface"].commands["vrf"].commands["unbind"], ["PortChannel0002"], obj=obj)
        print(result.exit_code, result.output)
        assert result.exit_code == 0
        assert 'PortChannel002' not in db.cfgdb.get_table('PORTCHANNEL_INTERFACE')
        assert result.output == expected_output_unbind
        
        expected_output_unbind = "Interface Eth32.10 IPv4 disabled and address(es) removed due to unbinding VRF."
        result = runner.invoke(config.config.commands["interface"].commands["vrf"].commands["unbind"], ["Eth32.10"], obj=obj)
        print(result.exit_code, result.output)
        assert result.exit_code == 0
        assert ('vrf_name', 'Vrf102') not in db.cfgdb.get_table('VLAN_SUB_INTERFACE')['Eth32.10']
        assert result.output == expected_output_unbind

        expected_output_unbind = "Interface Ethernet0.10 IPv4 disabled and address(es) removed due to unbinding VRF."
        result = runner.invoke(config.config.commands["interface"].commands["vrf"].commands["unbind"], ["Ethernet0.10"], obj=obj)
        print(result.exit_code, result.output)
        assert result.exit_code == 0
        assert ('vrf_name', 'Vrf101') not in db.cfgdb.get_table('VLAN_SUB_INTERFACE')['Ethernet0.10']
        assert result.output == expected_output_unbind

        expected_output_unbind = "Interface Po0002.101 IPv4 disabled and address(es) removed due to unbinding VRF."
        result = runner.invoke(config.config.commands["interface"].commands["vrf"].commands["unbind"], ["Po0002.101"], obj=obj)
        print(result.exit_code, result.output)
        assert result.exit_code == 0
        assert ('vrf_name', 'Vrf103') not in db.cfgdb.get_table('VLAN_SUB_INTERFACE')['Po0002.101']
        assert result.output == expected_output_unbind


        #Bind click CLI cannot be tested as it tries to connecte to statedb
        #for verification of all IP address delete before applying new vrf configuration
        jsonfile_config = os.path.join(mock_db_path, "config_db")
        dbconnector.dedicated_dbs['CONFIG_DB'] = jsonfile_config

        expected_output = """\
VRF     Interfaces
------  ---------------
Vrf1
Vrf101  Ethernet0.10
Vrf102  PortChannel0002
        Vlan40
        Eth32.10
Vrf103  Ethernet4
        Loopback0
        Po0002.101
"""
       
        result = runner.invoke(show.cli.commands['vrf'], [], obj=db)
        dbconnector.dedicated_dbs = {}
        assert result.exit_code == 0
        assert result.output == expected_output

    def test_vrf_del(self):
        from .mock_tables import dbconnector
        jsonfile_config = os.path.join(mock_db_path, "config_db")
        dbconnector.dedicated_dbs['CONFIG_DB'] = jsonfile_config
        runner = CliRunner()
        db = Db()   
        obj = {'config_db':db.cfgdb}

        expected_output_del_vrf = "VRF Vrf103 deleted and all associated IPv4 addresses removed."
        result = runner.invoke(config.config.commands["vrf"].commands["del"], ["Vrf103"], obj=obj)
        print(result.exit_code, result.output)
        assert result.exit_code == 0
        assert 'Ethernet4' not in db.cfgdb.get_table('INTERFACE')
        assert 'Loopback0' not in db.cfgdb.get_table('LOOPBACK_INTERFACE')
        assert ('vrf_name', 'Vrf103') not in db.cfgdb.get_table('VLAN_SUB_INTERFACE')['Po0002.101']
        assert 'Vrf103' not in db.cfgdb.get_table('VRF')
        assert result.output == expected_output_del_vrf

        expected_output_del_vrf = "VRF Vrf1 deleted and all associated IPv4 addresses removed."
        result = runner.invoke(config.config.commands["vrf"].commands["del"], ["Vrf1"], obj=obj)
        print(result.exit_code, result.output)
        assert result.exit_code == 0
        assert 'Vrf1' not in db.cfgdb.get_table('VRF')
        assert result.output == expected_output_del_vrf

    def test_vrf_bind(self):
        from .mock_tables import dbconnector
        jsonfile_config = os.path.join(mock_db_path, "config_db")
        dbconnector.dedicated_dbs['CONFIG_DB'] = jsonfile_config
        runner = CliRunner()
        db = Db()   
        obj = {'config_db':db.cfgdb}

        expected_output_bind = "Interface Ethernet8 IPv4 disabled and address(es) removed due to binding VRF Vrf101."
        result = runner.invoke(config.config.commands["interface"].commands["vrf"].commands["bind"], ["Ethernet8", "Vrf101"], obj=obj)
        print(result.exit_code, result.output)
        assert result.exit_code == 0
        assert ('Vrf101') in db.cfgdb.get_table('INTERFACE')['Ethernet8']['vrf_name']
        assert result.output == expected_output_bind