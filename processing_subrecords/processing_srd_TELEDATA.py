from work_byte_bit import hex_to_dec, param_byte, param_bit
from lists.types_subrecords import Tsr_EGTS_TELEDATA_SERVICE


# Обработки подзаписей сервиса.
def pr_EGTS_TELEDATA_SERVICE(srds, data_for_db):
    all_srds_srd = {}
    for srd in srds:
        dict_srd = srds[srd]
        all_srds_srd[srd] = {"SRD": {}}
        data_srd = {}

        dec_srt = hex_to_dec(dict_srd["SRT"])
        if dec_srt == Tsr_EGTS_TELEDATA_SERVICE.EGTS_SR_RECORD_RESPONSE.value:
            dict_srd["SRD"], data_srd["CRN"] = param_byte(dict_srd["SRD"], 2, True)
            dict_srd["SRD"], data_srd["RST"] = param_byte(dict_srd["SRD"], 1, False)

        # Это надо
        elif dec_srt == Tsr_EGTS_TELEDATA_SERVICE.EGTS_SR_POS_DATA.value:
            dict_srd["SRD"], data_srd["NTM"] = param_byte(dict_srd["SRD"], 4, True)
            dict_srd["SRD"], data_srd["LAT"] = param_byte(dict_srd["SRD"], 4, True)
            dict_srd["SRD"], data_srd["LONG"] = param_byte(dict_srd["SRD"], 4, True)
            dict_srd["SRD"], tmp_byte = param_byte(dict_srd["SRD"], 1, False)

            data_srd["ALTE"], data_srd["LOHS"], data_srd["LAHS"], data_srd["MV"], data_srd["BB"], data_srd["CS"], \
                data_srd["FIX"], data_srd["VLD"] = param_bit(tmp_byte, (1, 1, 1, 1, 1, 1, 1, 1))

            dict_srd["SRD"], data_srd["SPD0"] = param_byte(dict_srd["SRD"], 1, False)
            dict_srd["SRD"], tmp_byte = param_byte(dict_srd["SRD"], 1, False)

            data_srd["DIRH"], data_srd["ALTS"], data_srd["SPD1"] = param_bit(tmp_byte, (1, 1, 6))

            dict_srd["SRD"], data_srd["DIR"] = param_byte(dict_srd["SRD"], 1, False)
            dict_srd["SRD"], data_srd["ODM"] = param_byte(dict_srd["SRD"], 3, False)
            dict_srd["SRD"], data_srd["DIN"] = param_byte(dict_srd["SRD"], 1, False)
            dict_srd["SRD"], data_srd["SRC"] = param_byte(dict_srd["SRD"], 1, False)

            if int(data_srd["ALTE"]) == 1:
                dict_srd["SRD"], data_srd["ALT"] = param_byte(dict_srd["SRD"], 3, False)

            if hex_to_dec(data_srd["SRC"]) == 1:
                dict_srd["SRD"], data_srd["SRCD"] = param_byte(dict_srd["SRD"], 3, False)

            data_for_db.update_pos_data(hex_to_dec(data_srd["LAT"]),
                                        hex_to_dec(data_srd["LONG"]),
                                        int(data_srd["LOHS"]),
                                        int(data_srd["LAHS"]),
                                        int(data_srd["BB"]),
                                        int(data_srd["VLD"]),
                                        hex_to_dec(data_srd["SPD0"]),
                                        hex_to_dec(data_srd["DIR"]),
                                        0, #hex_to_dec(data_srd["SRC"]),
                                        hex_to_dec(data_srd["ALT"]) if "ALT" in data_srd else 0)

        # это надо
        elif dec_srt == Tsr_EGTS_TELEDATA_SERVICE.EGTS_SR_EXT_POS_DATA.value:
            dict_srd["SRD"], tmp_byte = param_byte(dict_srd["SRD"], 1, False)

            _, data_srd["NSFE"], data_srd["SFE"], data_srd["PFE"], data_srd["HFE"], data_srd["VFE"] = \
                param_bit(tmp_byte, (3, 1, 1, 1, 1, 1))

            if int(data_srd["VFE"]) == 1:
                dict_srd["SRD"], data_srd["VDOP"] = param_byte(dict_srd["SRD"], 2, True)

            if int(data_srd["HFE"]) == 1:
                dict_srd["SRD"], data_srd["HDOP"] = param_byte(dict_srd["SRD"], 2, True)

            if int(data_srd["PFE"]) == 1:
                dict_srd["SRD"], data_srd["PDOP"] = param_byte(dict_srd["SRD"], 2, True)

            if int(data_srd["SFE"]) == 1 or int(data_srd["NSFE"]) == 1:
                if int(data_srd["SFE"]) == 1:
                    dict_srd["SRD"], data_srd["SAT"] = param_byte(dict_srd["SRD"], 1, False)

                dict_srd["SRD"], data_srd["NS"] = param_byte(dict_srd["SRD"], 2, True)
        # это надо
        elif dec_srt == Tsr_EGTS_TELEDATA_SERVICE.EGTS_SR_AD_SENSORS_DATA.value:
            dict_srd["SRD"], tmp_byte = param_byte(dict_srd["SRD"], 1, False)
            bit_list_DIOE = param_bit(tmp_byte, (1, 1, 1, 1, 1, 1, 1, 1))

            data_srd["DIOE8"], data_srd["DIOE7"], data_srd["DIOE6"], data_srd["DIOE5"], data_srd["DIOE4"], \
                data_srd["DIOE3"], data_srd["DIOE2"], data_srd["DIOE1"] = bit_list_DIOE

            dict_srd["SRD"], data_srd["DOUT"] = param_byte(dict_srd["SRD"], 1, False)
            dict_srd["SRD"], tmp_byte = param_byte(dict_srd["SRD"], 1, False)
            bit_list_ASFE = param_bit(tmp_byte, (1, 1, 1, 1, 1, 1, 1, 1))

            data_srd["ASFE8"], data_srd["ASFE7"], data_srd["ASFE6"], data_srd["ASFE5"], data_srd["ASFE4"], \
                data_srd["ASFE3"], data_srd["ASFE2"], data_srd["ASFE1"] = bit_list_ASFE

            bit_list_DIOE = bit_list_DIOE[::-1]
            for ind_bit in range(len(bit_list_DIOE)):
                if int(bit_list_DIOE[ind_bit]) == 1:
                    dict_srd["SRD"], data_srd["ADIO{ind}".format(ind=ind_bit+1)] = param_byte(dict_srd["SRD"], 1, False)

            bit_list_ASFE = bit_list_ASFE[::-1]
            for ind_bit in range(len(bit_list_ASFE)):
                if int(bit_list_ASFE[ind_bit]) == 1:
                    dict_srd["SRD"], data_srd["ANS{ind}".format(ind=ind_bit + 1)] = param_byte(dict_srd["SRD"], 3, False)

        # это не надо
        elif dec_srt == Tsr_EGTS_TELEDATA_SERVICE.EGTS_SR_COUNTERS_DATA.value:
            # dict_srd["SRD"], tmp_byte = param_byte(dict_srd["SRD"], 1, False)
            # bit_list_CFE = param_bit(tmp_byte, (1, 1, 1, 1, 1, 1, 1, 1))
            #
            # data_srd["CFE8"], data_srd["CFE7"], data_srd["CFE6"], data_srd["CFE5"], data_srd["CFE4"], \
            #     data_srd["CFE3"], data_srd["CFE2"], data_srd["CFE1"] = bit_list_CFE
            #
            # bit_list_CFE = bit_list_CFE[::-1]
            # for ind_bit in range(len(bit_list_CFE)):
            #     if int(bit_list_CFE[ind_bit]) == 1:
            #         dict_srd["SRD"], data_srd[f"CN{ind_bit + 1}"] = param_byte(dict_srd["SRD"], 3, False)
            pass

        # это не надо. но оно используется хз.
        elif dec_srt == Tsr_EGTS_TELEDATA_SERVICE.EGTS_SR_ACCEL_DATA.value:
            dict_srd["SRD"], data_srd["SA"] = param_byte(dict_srd["SRD"], 1, False)
            dict_srd["SRD"], data_srd["ATM"] = param_byte(dict_srd["SRD"], 4, True)

            i = 0
            while len(dict_srd["SRD"]) > 0:
                i += 1
                srd_dict_data = {}
                dict_srd["SRD"], data_srd["ADS{i}".format(i=i)] = param_byte(dict_srd["SRD"], 8, False)

                data_srd["ADS{i}".format(i=i)], srd_dict_data["RTM"] = \
                    param_byte(data_srd["ADS{i}".format(i=i)], 2, True)
                data_srd["ADS{i}".format(i=i)], srd_dict_data["XAAV"] = \
                    param_byte(data_srd["ADS{i}".format(i=i)], 2, True)
                data_srd["ADS{i}".format(i=i)], srd_dict_data["YAAV"] = \
                    param_byte(data_srd["ADS{i}".format(i=i)], 2, True)
                data_srd["ADS{i}".format(i=i)], srd_dict_data["YAAV"] = \
                    param_byte(data_srd["ADS{i}".format(i=i)], 2, True)

                data_srd["ADS{i}".format(i=i)] = srd_dict_data

        # это не надо
        elif dec_srt == Tsr_EGTS_TELEDATA_SERVICE.EGTS_SR_STATE_DATA.value:
            pass
        # это не надо
        elif dec_srt == Tsr_EGTS_TELEDATA_SERVICE.EGTS_SR_LOOPIN_DATA.value:
            pass
        # это не надо
        elif dec_srt == Tsr_EGTS_TELEDATA_SERVICE.EGTS_SR_ABS_DIG_SENS_DATA.value:
            pass
        # это не надо
        elif dec_srt == Tsr_EGTS_TELEDATA_SERVICE.EGTS_SR_ABS_AN_SENS_DATA.value:
            pass

        # это надо
        elif dec_srt == Tsr_EGTS_TELEDATA_SERVICE.EGTS_SR_ABS_CNTR_DATA.value:
            dict_srd["SRD"], data_srd["CN"] = param_byte(dict_srd["SRD"], 1, False)
            dict_srd["SRD"], data_srd["CNV"] = param_byte(dict_srd["SRD"], 3, False)

        # это не надо
        elif dec_srt == Tsr_EGTS_TELEDATA_SERVICE.EGTS_SR_ABS_LOOPIN_DATA.value:
            pass

        # это надо.
        elif dec_srt == Tsr_EGTS_TELEDATA_SERVICE.EGTS_SR_LIQUID_LEVEL_SENSOR.value:
            dict_srd["SRD"], tmp_byte = param_byte(dict_srd["SRD"], 1, False)

            _, data_srd["LLSEF"], data_srd["LLSVU"], data_srd["RDF"], data_srd["LLSN"] = \
                param_bit(tmp_byte, (1, 1, 2, 1, 3))

            dict_srd["SRD"], data_srd["MADDR"] = param_byte(dict_srd["SRD"], 2, True)

            if int(data_srd["RDF"]) == 0:
                dict_srd["SRD"], data_srd["LLSD"] = param_byte(dict_srd["SRD"], 4, True)
            else:
                dict_srd["SRD"], data_srd["LLSD"] = param_byte(dict_srd["SRD"], len(dict_srd["SRD"]), False)

            if not int(data_srd["LLSEF"]):
                data_for_db.update_llsd(hex_to_dec(data_srd["LLSD"]))

        # это не надо
        elif dec_srt == Tsr_EGTS_TELEDATA_SERVICE.EGTS_SR_PASSENGERS_COUNTERS.value:
            pass

        all_srds_srd[srd]["SRD"] = data_srd

    return all_srds_srd
