from __future__ import annotations
import argparse, time, json, os, yaml
from datetime import datetime
from loguru import logger
from capture import capture_region, save_image
from schemas import ScreenshotMeta
from vision_llm import VisionTraderLLM
from referee import enforce
from executor import TraderExecutor
from state_machine import TraderStateMachine

def load_config(path: str):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config.yaml")
    parser.add_argument("--mode", choices=["dry-run","paper","live"], default="dry-run")
    parser.add_argument("--actuator", choices=["gui","broker"], default=None)
    args = parser.parse_args()

    cfg = load_config(args.config)
    if args.actuator:
        cfg["actuator"] = args.actuator
    mode = args.mode

    log_dir = cfg.get("log_dir","./logs")
    ensure_dir(log_dir)
    logger.add(os.path.join(log_dir, "session_{time}.log"), rotation="10 MB")

    region = cfg["screenshot_region"]
    interval_ms = int(cfg.get("capture_interval_ms", 1500))
    llm_provider = cfg.get("llm_provider", "mock")
    max_age_ms = int(cfg.get("max_image_age_ms", 2500))

    trader = TraderExecutor(mode=mode, actuator=cfg.get("actuator","gui"))
    fsm = TraderStateMachine()
    llm = VisionTraderLLM(provider=llm_provider)

    last_hash = None
    ensure_dir("./logs/images")

    logger.info(f"Starting Vision Trader in mode={mode}, actuator={cfg.get('actuator')} provider={llm_provider}")
    try:
        while True:
            img, meta = capture_region(region)
            # dedupe by hash
            if meta.hash == last_hash:
                time.sleep(interval_ms / 1000.0)
                continue
            # save image
            path = save_image(img, "./logs/images")
            meta.path = path

            chart, plan, decision = llm.analyze(path, meta)
            verdict, final_decision = enforce(cfg["risk"], max_age_ms, meta.timestamp, decision, plan)

            state = fsm.step(final_decision)

            # Persist a compact record
            rec = {
                "ts": datetime.utcnow().isoformat(),
                "image": path,
                "chart": chart.model_dump(),
                "plan": plan.model_dump(),
                "decision": final_decision.model_dump(),
                "verdict": verdict.model_dump(),
                "state": state,
            }
            with open(os.path.join(log_dir, "trace.jsonl"), "a") as f:
                f.write(json.dumps(rec) + "\n")

            # Execute
            trader.execute(final_decision)

            last_hash = meta.hash
            time.sleep(interval_ms / 1000.0)
    except KeyboardInterrupt:
        logger.warning("Kill switch activated; exiting.")

if __name__ == "__main__":
    main()
