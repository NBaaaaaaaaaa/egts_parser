from work_byte_bit import hex_to_dec, param_byte, param_bit, get_string
from lists.types_subrecords import Tsr_EGTS_AUTH_SERVICE


# Обработки подзаписей сервиса.
def pr_EGTS_AUTH_SERVICE(srds, data_for_db):
    all_srds_srd = {}
    for srd in srds:
        dict_srd = srds[srd]
        all_srds_srd[srd] = {"SRD": {}}
        data_srd = {}

        dec_srt = hex_to_dec(dict_srd["SRT"])
        if dec_srt == Tsr_EGTS_AUTH_SERVICE.EGTS_SR_RECORD_RESPONSE.value:
            dict_srd["SRD"], data_srd["CRN"] = param_byte(dict_srd["SRD"], 2, True)
            dict_srd["SRD"], data_srd["RST"] = param_byte(dict_srd["SRD"], 1, False)

        # это надо
        elif dec_srt == Tsr_EGTS_AUTH_SERVICE.EGTS_SR_TERM_IDENTITY.value:
            dict_srd["SRD"], data_srd["TID"] = param_byte(dict_srd["SRD"], 4, True)
            dict_srd["SRD"], tmp_byte = param_byte(dict_srd["SRD"], 1, False)
            data_srd["MNE"], data_srd["BSE"], data_srd["NIDE"], data_srd["SSRA"], data_srd["LNGCE"], \
                data_srd["IMSIE"], data_srd["IMEIE"], data_srd["HDIDE"] = param_bit(tmp_byte,
                                                                                    (1, 1, 1, 1, 1, 1, 1, 1))

            if int(data_srd["HDIDE"]) == 1:
                dict_srd["SRD"], data_srd["HDID"] = param_byte(dict_srd["SRD"], 2, True)

            if int(data_srd["IMEIE"]) == 1:
                dict_srd["SRD"], data_srd["IMEI"] = param_byte(dict_srd["SRD"], 15, False)
                data_srd["IMEI"] = str(data_srd["IMEI"])[2:-1]

            if int(data_srd["IMSIE"]) == 1:
                dict_srd["SRD"], data_srd["IMSI"] = param_byte(dict_srd["SRD"], 16, False)
                data_srd["IMSI"] = str(data_srd["IMSI"])[2:-1]

            if int(data_srd["LNGCE"]) == 1:
                dict_srd["SRD"], data_srd["LNGC"] = param_byte(dict_srd["SRD"], 3, False)
                data_srd["LNGC"] = str(data_srd["LNGC"])[2:-1]

            if int(data_srd["NIDE"]) == 1:
                dict_srd["SRD"], data_srd["NID"] = param_byte(dict_srd["SRD"], 3, False)
                _, data_srd["NID"]["MNC"], data_srd["NID"]["MCC"] = param_bit(data_srd["NID"], (4, 10, 10))

            dict_srd["SRD"], data_srd["BS"] = param_byte(dict_srd["SRD"], 2, True)
            dict_srd["SRD"], data_srd["MSISDN"] = param_byte(dict_srd["SRD"], 15, False)
            data_srd["MSISDN"] = str(data_srd["MSISDN"])[2:-1]

            if len(data_srd["MSISDN"]) == 0:
                data_srd["MSISDN"] = "000000000000000"

            data_for_db.update_auth(hex_to_dec(data_srd["TID"]), data_srd["IMEI"])

        # это не надо
        elif dec_srt == Tsr_EGTS_AUTH_SERVICE.EGTS_SR_MODULE_DATA.value:
            # dict_srd["SRD"], data_srd["MT"] = param_byte(dict_srd["SRD"], 1, False)
            # dict_srd["SRD"], data_srd["VID"] = param_byte(dict_srd["SRD"], 4, True)
            # dict_srd["SRD"], data_srd["FWV"] = param_byte(dict_srd["SRD"], 2, True)
            # dict_srd["SRD"], data_srd["SWV"] = param_byte(dict_srd["SRD"], 2, True)
            # dict_srd["SRD"], data_srd["MD"] = param_byte(dict_srd["SRD"], 1, False)
            # dict_srd["SRD"], data_srd["ST"] = param_byte(dict_srd["SRD"], 1, False)
            #
            # dict_srd["SRD"], data_srd["SRN"], data_srd["D1"] = get_string(dict_srd["SRD"])
            # dict_srd["SRD"], data_srd["DSCR"], data_srd["D2"] = get_string(dict_srd["SRD"])
            pass
        # это не надо
        elif dec_srt == Tsr_EGTS_AUTH_SERVICE.EGTS_SR_VEHICLE_DATA.value:
            # dict_srd["SRD"], data_srd["VIN"] = param_byte(dict_srd["SRD"], 17, False)
            # data_srd["VIN"] = str(data_srd["VIN"])[2:-1]
            # dict_srd["SRD"], data_srd["VHT"] = param_byte(dict_srd["SRD"], 4, True)
            # dict_srd["SRD"], data_srd["VPST"] = param_byte(dict_srd["SRD"], 4, True)
            pass
        # это не надо
        elif dec_srt == Tsr_EGTS_AUTH_SERVICE.EGTS_SR_AUTH_PARAMS.value:
            # dict_srd["SRD"], tmp_byte = param_byte(dict_srd["SRD"], 1, False)
            # _, data_srd["EXE"], data_srd["SSE"], data_srd["MSE"], data_srd["ISLE"], \
            #     data_srd["PKE"], data_srd["ENA"] = param_bit(tmp_byte, (1, 1, 1, 1, 1, 1, 2))
            #
            # if int(data_srd["PKE"]) == 1:
            #     dict_srd["SRD"], data_srd["PKL"] = param_byte(dict_srd["SRD"], 2, True)
            #     dict_srd["SRD"], data_srd["PBK"] = param_byte(dict_srd["SRD"], hex_to_dec(data_srd["PKL"]), False)
            #
            # if int(data_srd["ISLE"]) == 1:
            #     dict_srd["SRD"], data_srd["ISL"] = param_byte(dict_srd["SRD"], 2, True)
            #
            # if int(data_srd["MSE"]) == 1:
            #     dict_srd["SRD"], data_srd["MSZ"] = param_byte(dict_srd["SRD"], 2, True)
            #
            # if int(data_srd["SSE"]) == 1:
            #     dict_srd["SRD"], data_srd["SS"], data_srd["D1"] = get_string(dict_srd["SRD"])
            #
            # if int(data_srd["EXE"]) == 1:
            #     dict_srd["SRD"], data_srd["EXP"], data_srd["D2"] = get_string(dict_srd["SRD"])

            # стр 52 есть продолжение обработки
            pass
        # это не надо
        elif dec_srt == Tsr_EGTS_AUTH_SERVICE.EGTS_SR_AUTH_INFO.value:
            # dict_srd["SRD"], data_srd["UNM"], data_srd["D1"] = get_string(dict_srd["SRD"])
            # dict_srd["SRD"], data_srd["UPSW"], data_srd["D2"] = get_string(dict_srd["SRD"])
            # dict_srd["SRD"], data_srd["SS"], data_srd["D3"] = get_string(dict_srd["SRD"])
            pass
        # это не надо
        elif dec_srt == Tsr_EGTS_AUTH_SERVICE.EGTS_SR_SERVICE_INFO.value:
            # dict_srd["SRD"], data_srd["ST"] = param_byte(dict_srd["SRD"], 1, False)
            # dict_srd["SRD"], data_srd["SST"] = param_byte(dict_srd["SRD"], 1, False)
            # dict_srd["SRD"], data_srd["SRVP"] = param_byte(dict_srd["SRD"], 1, False)
            # data_srd["SRVA"], _, data_srd["ST"] = param_bit(dict_srd["SRD"], (1, 5, 2))

            # стр 54
            pass
        # это не надо
        elif dec_srt == Tsr_EGTS_AUTH_SERVICE.EGTS_SR_RESULT_CODE.value:
            # dict_srd["SRD"], data_srd["RCD"] = param_byte(dict_srd["SRD"], 1, False)
            pass

        all_srds_srd[srd]["SRD"] = data_srd

    return all_srds_srd
