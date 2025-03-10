API_VERSION = 'API_v1.0'  # This is Mandatory!
MOD_NAME = 'ArmorInfo'  # Your Mod Name
from DataEnum import TestEnum

try:
    import battle, events, dataHub, ui, constants, utils, callbacks
except:
    pass


class ArmorInfo(object):
    def __init__(self):
        self._testEnum = TestEnum
        self._cacheSet = {}
        self._defSet = {'citadel': 'N/A', 'bow_st': 'N/A', 'cas': 'N/A', 'cas_deck': 'N/A',
                        'outer': 'N/A', 'dd_cas': 'N/A', 'cas_t': 'N/A', 'bow_st_s': 'N/A'}
        self._cacheIDS = None
        events.onBattleShown(self.onBattleStart)
        self._vary = None
        self._targetPlayerName = None
        self._isObserver = False
        self._uiId = None

    def onBattleStart(self, *args):
        self._uiId = uiId = ui.createUiElement()
        ui.addDataComponentWithId(uiId, 'ArmorInfoModEntityKey', {})
        self._vary = callbacks.callback(0.1, self.getTargetShip)
        self._isObserver = battle.isObserverMode()

    def onQuit(self, *args):
        callbacks.cancel(self._vary)
        self._vary = None
        self._targetPlayerName = None
        self._cacheSet = {}
        self._cacheIDS = None
        ui.deleteUiElement(self._uiId)
        self._isObserver = False

    def getTargetShip(self, *args, **kwargs):
        # GetObserverShipIDS reference DamageMonitor
        try:
            target = battle.getObserverShip()
        except:
            target = None

        if target is None and not self._isObserver:
            target = battle.getSelfPlayerShip()

        pName = target.playerName if target else None
        if self._targetPlayerName != pName:
            targetPlayerInfo = battle.getPlayerInfoByName(pName)
            self._targetPlayerName = pName
            targetShipIDS = targetPlayerInfo.shipInfo.shortName if pName else None
            shipType = targetPlayerInfo.shipInfo.subtype if pName else None

            if targetShipIDS == self._cacheIDS:
                armorInfo = self._cacheSet.copy()
            else:
                getInfo = getattr(self._testEnum, targetShipIDS, self._defSet)
                processed_dict = {}
                for key, value in getInfo.items():
                    processed_dict[key] = str(value) if value and value != '0' else 'N/A'
                armorInfo = processed_dict
                self._cacheIDS = targetShipIDS
                self._cacheSet = armorInfo.copy()

            ui.updateUiElementData(self._uiId, dict(
                shipIDS='IDS_' + targetShipIDS,
                shipType=shipType,
                citadel=armorInfo["citadel"],
                bow_st=armorInfo["bow_st"],
                cas=armorInfo["cas"],
                cas_deck=armorInfo["cas_deck"],
                outer=armorInfo["outer"],
                dd_cas=armorInfo["dd_cas"],
                cas_t=armorInfo["cas_t"],
                bow_st_s=armorInfo['bow_st_s'],
            ))


ArmorInfoMod = ArmorInfo()
