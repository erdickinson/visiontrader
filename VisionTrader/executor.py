from __future__ import annotations
from loguru import logger
from schemas import ActionDecision, OrderSpec

class TraderExecutor:
    def __init__(self, mode: str = "dry-run", actuator: str = "gui"):
        self.mode = mode
        self.actuator = actuator

    def execute(self, decision: ActionDecision):
        action = decision.action
        logger.info(f"Executor received action={action} reason={decision.reason}")
        if action in ("WAIT", "CANCEL"):
            return
        if action == "ARM":
            # Prepare order ticket or set intent
            logger.info("Arming trade (no order yet).")
            return
        if action == "ENTER":
            return self._enter(decision.order)
        if action == "ADJUST":
            return self._adjust(decision.order)
        if action == "EXIT":
            return self._exit()

    # --- Actuator methods (stubs) ---
    def _enter(self, order: OrderSpec | None):
        if self.mode == "dry-run":
            logger.info(f"[DRY-RUN] Would ENTER: {order}")
            return
        if self.actuator == "gui":
            return self._gui_click(order)
        if self.actuator == "broker":
            return self._broker_place(order)

    def _adjust(self, order: OrderSpec | None):
        if self.mode == "dry-run":
            logger.info(f"[DRY-RUN] Would ADJUST: {order}")
            return
        # Implement GUI or broker adjust
        logger.info("Adjusting order (stub).")

    def _exit(self):
        if self.mode == "dry-run":
            logger.info("[DRY-RUN] Would EXIT position")
            return
        logger.info("Exiting position (stub).")

    def _gui_click(self, order: OrderSpec | None):
        # Implement with pyautogui if you insist on clicking the DOM/window.
        # Safer alternative: hotkeys/macros in your platform to standardize order placement.
        logger.info("[GUI] Clicker stub called. Map your hotkeys here.")
        # e.g., pyautogui.typewrite(...), pyautogui.press(...)

    def _broker_place(self, order: OrderSpec | None):
        # Replace with your broker connector (IB, Alpaca, Tradovate, etc.).
        logger.info("[BROKER] Stub place order. Implement your API client here.")
