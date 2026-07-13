API_VERSION = 'API_v1.0'
MOD_NAME = 'ArmorInfo'

from DataEnum import EnumX, EnumIX, EnumVIII, EnumEX, EnumVII, EnumVI, EnumV, EnumIV, EnumIII

try:
    import battle, callbacks, events, ui
except:
    pass


class ArmorInfo(object):
    def __init__(self):
        self._enumX = EnumX
        self._enumIX = EnumIX
        self._enumVIII = EnumVIII
        self._enumVII = EnumVII
        self._enumVI = EnumVI
        self._enumV = EnumV
        self._enumIV = EnumIV
        self._enumIII = EnumIII
        self._enumEX = EnumEX
        self._cacheSet = {}
        self._defSet = {'citadel': 'N/A', 'bow_st': 'N/A', 'cas': 'N/A', 'cas_deck': 'N/A',
                        'outer': 'N/A', 'dd_cas': 'N/A', 'cas_t': 'N/A', 'bow_st_s': 'N/A'}
        self._cacheIDS = None
        events.onBattleShown(self.onBattleStart)
        events.onBattleQuit(self.onQuit)
        self._vary = None
        self._targetPlayerName = None
        self._isObserver = False
        self._uiId = None

    def onBattleStart(self, *args):
        self._cancelTargetCallback()
        if self._uiId is not None:
            ui.deleteUiElement(self._uiId)

        self._targetPlayerName = None
        self._uiId = uiId = ui.createUiElement()
        ui.addDataComponentWithId(uiId, 'ArmorInfoModEntityKey', {})
        self._isObserver = battle.isObserverMode()
        self._vary = callbacks.callback(0.1, self.getTargetShip)

    def onQuit(self, *args):
        self._cancelTargetCallback()
        self._targetPlayerName = None
        self._cacheSet = {}
        self._cacheIDS = None
        if self._uiId is not None:
            ui.deleteUiElement(self._uiId)
            self._uiId = None
        self._isObserver = False

    def _cancelTargetCallback(self):
        if self._vary is not None:
            callbacks.cancel(self._vary)
            self._vary = None

    def getTargetShip(self, *args, **kwargs):
        # GetObserverShipIDS reference DamageMonitor
        try:
            target = battle.getObserverShip()
        except:
            target = None

        if target is None and not self._isObserver:
            target = battle.getSelfPlayerShip()

        playerName = target.playerName if target else None
        if self._targetPlayerName == playerName:
            return

        if playerName is None:
            self._targetPlayerName = None
            if self._uiId is not None:
                ui.updateUiElementData(self._uiId, {})
            return

        targetPlayerInfo = battle.getPlayerInfoByName(playerName)
        if targetPlayerInfo is None or targetPlayerInfo.shipInfo is None:
            return

        self._targetPlayerName = playerName
        targetShipIDS = targetPlayerInfo.shipInfo.shortName
        shipType = targetPlayerInfo.shipInfo.subtype
        shipLv = targetPlayerInfo.shipInfo.level

        if targetShipIDS == self._cacheIDS:
            armorInfo = self._cacheSet.copy()
        else:
            getInfo = getattr(self.getEnumByLevel(shipLv, shipType), targetShipIDS, self._defSet)
            processedInfo = {}
            for key, value in getInfo.items():
                processedInfo[key] = str(value) if value and value != '0' else 'N/A'
            armorInfo = processedInfo
            self._cacheIDS = targetShipIDS
            self._cacheSet = armorInfo.copy()

        if self._uiId is not None:
            ui.updateUiElementData(self._uiId, dict(
                shipIDS='IDS_' + targetShipIDS,
                shipType=shipType,
                citadel=armorInfo['citadel'],
                bow_st=armorInfo['bow_st'],
                cas=armorInfo['cas'],
                cas_deck=armorInfo['cas_deck'],
                outer=armorInfo['outer'],
                dd_cas=armorInfo['dd_cas'],
                cas_t=armorInfo['cas_t'],
                bow_st_s=armorInfo['bow_st_s'],
            ))

    def getEnumByLevel(self, lv, shipType):
        if lv == 11 or shipType == 'AirCarrier':
            return self._enumEX
        elif lv == 10:
            return self._enumX
        elif lv == 9:
            return self._enumIX
        elif lv == 8:
            return self._enumVIII
        elif lv == 7:
            return self._enumVII
        elif lv == 6:
            return self._enumVI
        elif lv == 5:
            return self._enumV
        elif lv == 4:
            return self._enumIV
        elif lv == 3:
            return self._enumIII
        else:
            return self._defSet

ArmorInfoMod = ArmorInfo()
