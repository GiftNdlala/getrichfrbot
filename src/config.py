import json
import os
from typing import Any, Dict
from dotenv import load_dotenv
import pytz

_CONFIG_CACHE: Dict[str, Any] = {}


def _load_file_config() -> Dict[str, Any]:
	path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
	if not os.path.exists(path):
		return {}
	with open(path, 'r') as f:
		return json.load(f)


def _merge_env(cfg: Dict[str, Any]) -> Dict[str, Any]:
	# Broker env overrides
	broker = cfg.setdefault('broker', {})
	broker['server'] = os.getenv('MT5_SERVER', broker.get('server'))
	login_env = os.getenv('MT5_LOGIN')
	if login_env:
		try:
			broker['login'] = int(login_env)
		except ValueError:
			pass
	broker['symbol'] = os.getenv('MT5_SYMBOL', broker.get('symbol', 'XAUUSD'))

	# Secrets
	cfg.setdefault('secrets_env', {}).setdefault('mt5_password_env', 'MT5_PASSWORD')

	# Sessions timezone
	sessions = cfg.setdefault('sessions', {})
	sessions['timezone'] = os.getenv('APP_TIMEZONE', sessions.get('timezone', 'Africa/Johannesburg'))

	return cfg


def get_config(refresh: bool = False) -> Dict[str, Any]:
	global _CONFIG_CACHE
	if _CONFIG_CACHE and not refresh:
		return _CONFIG_CACHE
	load_dotenv()  # load .env
	cfg = _load_file_config()
	cfg = _merge_env(cfg)
	# Validate timezone
	try:
		_ = pytz.timezone(cfg.get('sessions', {}).get('timezone', 'Africa/Johannesburg'))
	except Exception:
		cfg['sessions']['timezone'] = 'Africa/Johannesburg'
	_CONFIG_CACHE = cfg
	return cfg