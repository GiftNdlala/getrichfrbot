PS C:\Users\ndlal\getrichfrbot> python shell
C:\Users\ndlal\AppData\Local\Programs\Python\Python311\python.exe: can't open file 'C:\\Users\\ndlal\\getrichfrbot\\shell': [Errno 2] No such file or directory
PS C:\Users\ndlal\getrichfrbot> $resp.trades |
>>   Where-Object symbol -eq 'XAUUSDm' |
>>   Select-Object timestamp, engine, direction, entry, sl, tp, status, ticket |
>>   Format-Table -AutoSize
PS C:\Users\ndlal\getrichfrbot> $resp.trades |
>>   Where-Object symbol -eq 'XAUUSDm' |
>>   Select-Object timestamp, engine, direction, entry, sl, tp, status, ticket |
>>   Format-Table -AutoSize
PS C:\Users\ndlal\getrichfrbot> Invoke-RestMethod "http://localhost:5000/api/recent_trades?hours=6&limit=200" |
>>   ConvertTo-Json -Depth 6
{
    "count":  200,
    "hours":  6,
    "status":  "success",
    "trades":  [
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "SWING_HIGH",
                       "entry":  3970.6419428571426,
                       "id":  4246,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T09:55:31.132309",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3971.3002857142856,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1894326394,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 11:57:41",
                       "tp":  3966.6419428571426
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "SWING_HIGH",
                       "entry":  3970.074507142857,
                       "id":  4245,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T09:48:54.801238",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3971.037714285714,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1894295112,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 11:51:04",
                       "tp":  3966.074507142857
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "SWING_HIGH",
                       "entry":  3970.3144964285716,
                       "id":  4244,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T09:47:23.797534",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3971.278142857143,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1894288949,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 11:49:33",
                       "tp":  3966.3144964285716
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "SWING_HIGH",
                       "entry":  3969.1045107142854,
                       "id":  4243,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T09:44:51.328431",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3969.903571428571,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1894275593,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 11:47:01",
                       "tp":  3965.1045107142854
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "SWING_HIGH",
                       "entry":  3970.251021428571,
                       "id":  4242,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T09:38:12.723554",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3972.3821428571428,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1894245071,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 11:40:22",
                       "tp":  3966.251021428571
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "SWING_HIGH",
                       "entry":  3969.6093214285715,
                       "id":  4241,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T09:37:42.029236",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3971.646142857143,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1894241689,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 11:39:51",
                       "tp":  3965.6093214285715
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "SWING_HIGH",
                       "entry":  3967.8625821428573,
                       "id":  4240,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T09:37:11.409400",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3969.642714285714,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1894238494,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 11:39:20",
                       "tp":  3963.8625821428573
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "SWING_HIGH",
                       "entry":  3968.0893892857143,
                       "id":  4239,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T09:36:41.031417",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3969.8364285714288,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1894236302,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 11:38:50",
                       "tp":  3964.0893892857143
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "SWING_HIGH",
                       "entry":  3967.6788607142853,
                       "id":  4238,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T09:36:10.443226",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3969.3655714285715,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1894234413,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 11:38:19",
                       "tp":  3963.6788607142853
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "SWING_HIGH",
                       "entry":  3967.7350607142857,
                       "id":  4237,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T09:35:39.698423",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3969.4135714285712,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1894231964,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 11:37:50",
                       "tp":  3963.7350607142857
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "SWING_HIGH",
                       "entry":  3968.0448071428573,
                       "id":  4236,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T09:35:08.830742",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3969.6927142857144,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1894228797,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 11:37:15",
                       "tp":  3964.0448071428573
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "SWING_HIGH",
                       "entry":  3969.0379107142858,
                       "id":  4235,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T09:34:35.383919",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3970.6405714285715,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1894225289,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 11:36:44",
                       "tp":  3965.0379107142858
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "SWING_HIGH",
                       "entry":  3969.049039285714,
                       "id":  4234,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T09:34:04.219932",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3970.6874285714284,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1894223112,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 11:36:14",
                       "tp":  3965.049039285714
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "SWING_HIGH",
                       "entry":  3969.109346428572,
                       "id":  4233,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T09:33:28.571518",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3970.981142857143,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1894220914,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 11:35:31",
                       "tp":  3965.109346428572
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "SWING_HIGH",
                       "entry":  3972.90385,
                       "id":  4232,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T09:18:13.893697",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3974.222,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1894102564,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 11:16:37",
                       "tp":  3968.90385
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "SWING_HIGH",
                       "entry":  3977.290503571429,
                       "id":  4231,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T09:11:47.280614",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3978.130857142857,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1894063514,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 11:11:06",
                       "tp":  3973.290503571429
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "SWING_HIGH",
                       "entry":  3978.319075,
                       "id":  4230,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T09:00:05.130695",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3979.505,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893990149,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 11:02:13",
                       "tp":  3974.319075
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "SWING_HIGH",
                       "entry":  3978.5380571428573,
                       "id":  4229,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T08:59:32.805516",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3979.7657142857142,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893987892,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 11:01:42",
                       "tp":  3974.5380571428573
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "SWING_HIGH",
                       "entry":  3978.101532142857,
                       "id":  4228,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T08:59:02.368738",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3979.309714285714,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893985901,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 11:01:13",
                       "tp":  3974.101532142857
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "SWING_HIGH",
                       "entry":  3977.992357142857,
                       "id":  4227,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T08:58:32.085154",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3979.2077142857142,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893983139,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 11:00:42",
                       "tp":  3973.992357142857
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "SWING_HIGH",
                       "entry":  3980.0518178571433,
                       "id":  4226,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T08:57:31.178862",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3981.0842857142857,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893974499,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 10:59:41",
                       "tp":  3976.0518178571433
                   },
                   {
                       "alert_level":  "MEDIUM",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "INTRADAY_MED",
                       "entry":  3981.262242857143,
                       "id":  4225,
                       "lots":  0.02,
                       "open_time":  "2025-11-05T08:50:48.597126",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3980.6347142857144,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893939603,
                       "tier":  "",
                       "timestamp":  "2025-11-05 10:52:59",
                       "tp":  3988.262242857143
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "SWING_HIGH",
                       "entry":  3980.884128571429,
                       "id":  4224,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T08:49:47.949496",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3981.739857142857,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893934332,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 10:51:57",
                       "tp":  3976.884128571429
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "SWING_HIGH",
                       "entry":  3980.279582142857,
                       "id":  4223,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T08:48:43.246548",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3981.1987142857142,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893928704,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 10:50:43",
                       "tp":  3976.279582142857
                   },
                   {
                       "alert_level":  "MEDIUM",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "INTRADAY_MED",
                       "entry":  3982.8082464285712,
                       "id":  4222,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T08:41:05.335203",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3983.6066071428572,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893894289,
                       "tier":  "",
                       "timestamp":  "2025-11-05 10:43:16",
                       "tp":  3975.8082464285712
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3984.2207285714285,
                       "id":  4221,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T08:40:35.026614",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3983.3298571428572,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893891943,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 10:42:45",
                       "tp":  3988.2207285714285
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3984.4633357142857,
                       "id":  4220,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T08:40:04.655153",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3983.5065714285715,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893889872,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 10:42:15",
                       "tp":  3988.4633357142857
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3984.4918071428574,
                       "id":  4219,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T08:39:34.348825",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3983.4747142857145,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893887980,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 10:41:44",
                       "tp":  3988.4918071428574
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3984.4165892857145,
                       "id":  4218,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T08:39:03.976861",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3983.3674285714287,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893885526,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 10:41:14",
                       "tp":  3988.4165892857145
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3984.7924392857144,
                       "id":  4217,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T08:37:43.485198",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3983.6264285714287,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893878491,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 10:39:53",
                       "tp":  3988.7924392857144
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3984.8603035714286,
                       "id":  4216,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T08:37:13.115309",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3983.6588571428574,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893876080,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 10:39:23",
                       "tp":  3988.8603035714286
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3984.958207142857,
                       "id":  4215,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T08:36:42.759311",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3983.555714285714,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893872631,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 10:38:53",
                       "tp":  3988.958207142857
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3984.8227464285715,
                       "id":  4214,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T08:36:12.458454",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3983.398142857143,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893869719,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 10:38:22",
                       "tp":  3988.8227464285715
                   },
                   {
                       "alert_level":  "LOW",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "INTRADAY_LOW",
                       "entry":  3982.824964285714,
                       "id":  4213,
                       "lots":  0.02,
                       "open_time":  "2025-11-05T08:35:11.874140",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3983.497714285714,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893864815,
                       "tier":  "",
                       "timestamp":  "2025-11-05 10:37:22",
                       "tp":  3978.824964285714
                   },
                   {
                       "alert_level":  "MEDIUM",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "INTRADAY_MED",
                       "entry":  3981.2576357142857,
                       "id":  4212,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T08:29:39.089073",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3980.1529285714287,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893833067,
                       "tier":  "",
                       "timestamp":  "2025-11-05 10:31:49",
                       "tp":  3988.2576357142857
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "SWING_HIGH",
                       "entry":  3980.139842857143,
                       "id":  4211,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T08:28:38.595353",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3981.5402857142853,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893828159,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 10:30:48",
                       "tp":  3976.139842857143
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "SWING_HIGH",
                       "entry":  3980.548760714286,
                       "id":  4210,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T08:28:08.259522",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3982.0345714285713,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893825577,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 10:30:18",
                       "tp":  3976.548760714286
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "SWING_HIGH",
                       "entry":  3979.5524571428573,
                       "id":  4209,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T08:27:37.945508",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3981.0097142857144,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893821286,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 10:29:47",
                       "tp":  3975.5524571428573
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "SWING_HIGH",
                       "entry":  3978.9951535714285,
                       "id":  4208,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T08:27:07.546323",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3980.3828571428567,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893818402,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 10:29:17",
                       "tp":  3974.9951535714285
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "SWING_HIGH",
                       "entry":  3980.0591857142854,
                       "id":  4207,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T08:26:37.092557",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3981.445571428571,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893815386,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 10:28:47",
                       "tp":  3976.0591857142854
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "SWING_HIGH",
                       "entry":  3979.305017857143,
                       "id":  4206,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T08:26:06.765226",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3980.7392857142854,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893811630,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 10:28:16",
                       "tp":  3975.305017857143
                   },
                   {
                       "alert_level":  "LOW",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "INTRADAY_LOW",
                       "entry":  3979.2713392857145,
                       "id":  4205,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T08:25:36.416865",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3978.4662142857146,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893808460,
                       "tier":  "",
                       "timestamp":  "2025-11-05 10:27:46",
                       "tp":  3983.2713392857145
                   },
                   {
                       "alert_level":  "LOW",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "INTRADAY_LOW",
                       "entry":  3980.266628571429,
                       "id":  4204,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T08:19:28.347439",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3979.5184285714286,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893770609,
                       "tier":  "",
                       "timestamp":  "2025-11-05 10:21:37",
                       "tp":  3984.266628571429
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3983.9891714285714,
                       "id":  4203,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T08:16:55.710469",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3982.342142857143,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893756437,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 10:19:05",
                       "tp":  3987.9891714285714
                   },
                   {
                       "alert_level":  "MEDIUM",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "INTRADAY_MED",
                       "entry":  3984.4834464285714,
                       "id":  4201,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T08:10:25.165422",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3981.8656071428572,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893716809,
                       "tier":  "",
                       "timestamp":  "2025-11-05 10:12:34",
                       "tp":  3991.4834464285714
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "FARMER",
                       "entry":  3984.4834464285714,
                       "id":  4202,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T08:10:25.486535",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  "TIME",
                       "sl":  3966.4834464285714,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893716855,
                       "tier":  "FARMER",
                       "timestamp":  "2025-11-05 10:12:34",
                       "tp":  3986.4834464285714
                   },
                   {
                       "alert_level":  "MEDIUM",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "INTRADAY_MED",
                       "entry":  3981.66545,
                       "id":  4199,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T08:09:54.361074",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3984.0385,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893713574,
                       "tier":  "",
                       "timestamp":  "2025-11-05 10:12:04",
                       "tp":  3974.66545
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "FARMER",
                       "entry":  3981.66545,
                       "id":  4200,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T08:09:54.523186",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3999.66545,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893713583,
                       "tier":  "FARMER",
                       "timestamp":  "2025-11-05 10:12:04",
                       "tp":  3979.66545
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3982.8184107142856,
                       "id":  4198,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T08:09:23.725320",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3979.7265714285713,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893710154,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 10:11:33",
                       "tp":  3986.8184107142856
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3986.436603571429,
                       "id":  4197,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T08:07:51.243160",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3983.6648571428573,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893700050,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 10:10:00",
                       "tp":  3990.436603571429
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3985.5940571428573,
                       "id":  4196,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T08:07:20.521440",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3982.9267142857143,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893695507,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 10:09:31",
                       "tp":  3989.5940571428573
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3986.150425,
                       "id":  4195,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T08:06:50.160640",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3983.55,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893692255,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 10:08:54",
                       "tp":  3990.150425
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3984.0667714285714,
                       "id":  4194,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T08:05:44.541106",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3981.616142857143,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893683036,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 10:07:51",
                       "tp":  3988.0667714285714
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3985.4036107142856,
                       "id":  4193,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T08:05:10.478362",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3983.1235714285713,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893678665,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 10:07:19",
                       "tp":  3989.4036107142856
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3984.514682142857,
                       "id":  4192,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T08:04:38.287237",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3982.354714285714,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893673876,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 10:06:47",
                       "tp":  3988.514682142857
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3982.2249642857146,
                       "id":  4191,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T08:04:07.650807",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3980.3404285714287,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893668999,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 10:06:17",
                       "tp":  3986.2249642857146
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3977.0433357142856,
                       "id":  4190,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T08:03:01.807433",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3975.7175714285713,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893652676,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 10:05:09",
                       "tp":  3981.0433357142856
                   },
                   {
                       "alert_level":  "MEDIUM",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "INTRADAY_MED",
                       "entry":  3974.748410714286,
                       "id":  4188,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T08:02:29.420579",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3973.9296785714287,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893647442,
                       "tier":  "",
                       "timestamp":  "2025-11-05 10:04:34",
                       "tp":  3981.748410714286
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "FARMER",
                       "entry":  3974.748410714286,
                       "id":  4189,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T08:02:29.694488",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3956.748410714286,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893647475,
                       "tier":  "FARMER",
                       "timestamp":  "2025-11-05 10:04:34",
                       "tp":  3976.748410714286
                   },
                   {
                       "alert_level":  "MEDIUM",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "INTRADAY_MED",
                       "entry":  3974.2497285714285,
                       "id":  4186,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T08:01:58.249723",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3975.0641428571425,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893644414,
                       "tier":  "",
                       "timestamp":  "2025-11-05 10:04:06",
                       "tp":  3967.2497285714285
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "FARMER",
                       "entry":  3974.2497285714285,
                       "id":  4187,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T08:01:58.468832",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  "TIME",
                       "sl":  3992.2497285714285,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893644465,
                       "tier":  "FARMER",
                       "timestamp":  "2025-11-05 10:04:06",
                       "tp":  3972.2497285714285
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3973.623085714286,
                       "id":  4185,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T08:01:27.213140",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3972.4305714285715,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893640962,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 10:03:36",
                       "tp":  3977.623085714286
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3974.293985714286,
                       "id":  4184,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T08:00:56.537228",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3973.1465714285714,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893638295,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 10:03:06",
                       "tp":  3978.293985714286
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3975.060457142857,
                       "id":  4183,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T08:00:26.065071",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3973.9757142857143,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893635764,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 10:02:35",
                       "tp":  3979.060457142857
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3975.188160714286,
                       "id":  4182,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T07:59:55.554398",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3974.0745714285713,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893633648,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 10:02:06",
                       "tp":  3979.188160714286
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3975.0888178571427,
                       "id":  4181,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T07:59:25.092919",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3973.9072857142855,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893630582,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 10:01:33",
                       "tp":  3979.0888178571427
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3973.421375,
                       "id":  4180,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T07:56:48.778805",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3972.422,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893614700,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 09:58:59",
                       "tp":  3977.421375
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3973.8235,
                       "id":  4179,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T07:56:18.322645",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3972.819,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893612848,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 09:58:29",
                       "tp":  3977.8235
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3973.9328,
                       "id":  4178,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T07:55:47.614179",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3972.875,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893610292,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 09:57:58",
                       "tp":  3977.9328
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3972.685785714286,
                       "id":  4177,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T07:55:17.053929",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3971.7515714285714,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893605886,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 09:57:26",
                       "tp":  3976.685785714286
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3972.0549892857143,
                       "id":  4176,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T07:54:46.074142",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3971.1534285714283,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893602296,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 09:56:56",
                       "tp":  3976.0549892857143
                   },
                   {
                       "alert_level":  "MEDIUM",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "INTRADAY_MED",
                       "entry":  3971.648603571429,
                       "id":  4174,
                       "lots":  0.02,
                       "open_time":  "2025-11-05T07:54:15.112700",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3970.947892857143,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893600183,
                       "tier":  "",
                       "timestamp":  "2025-11-05 09:56:25",
                       "tp":  3978.648603571429
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "FARMER",
                       "entry":  3971.648603571429,
                       "id":  4175,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T07:54:15.466736",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3953.648603571429,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893600286,
                       "tier":  "FARMER",
                       "timestamp":  "2025-11-05 09:56:25",
                       "tp":  3973.648603571429
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3970.1754071428572,
                       "id":  4173,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T07:53:44.753061",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3969.3797142857143,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893598340,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 09:55:54",
                       "tp":  3974.1754071428572
                   },
                   {
                       "alert_level":  "MEDIUM",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "INTRADAY_MED",
                       "entry":  3970.4757821428575,
                       "id":  4171,
                       "lots":  0.02,
                       "open_time":  "2025-11-05T07:52:12.422688",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3969.862535714286,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893592991,
                       "tier":  "",
                       "timestamp":  "2025-11-05 09:54:21",
                       "tp":  3977.4757821428575
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "FARMER",
                       "entry":  3970.4757821428575,
                       "id":  4172,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T07:52:12.751223",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3952.4757821428575,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893593010,
                       "tier":  "FARMER",
                       "timestamp":  "2025-11-05 09:54:21",
                       "tp":  3972.4757821428575
                   },
                   {
                       "alert_level":  "MEDIUM",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "INTRADAY_MED",
                       "entry":  3971.0412535714286,
                       "id":  4169,
                       "lots":  0.02,
                       "open_time":  "2025-11-05T07:51:41.402897",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3970.413392857143,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893591635,
                       "tier":  "",
                       "timestamp":  "2025-11-05 09:53:51",
                       "tp":  3978.0412535714286
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "FARMER",
                       "entry":  3971.0412535714286,
                       "id":  4170,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T07:51:41.558356",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3953.0412535714286,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893591650,
                       "tier":  "FARMER",
                       "timestamp":  "2025-11-05 09:53:51",
                       "tp":  3973.0412535714286
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3970.285989285714,
                       "id":  4168,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T07:51:10.934006",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3969.5074285714286,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893590339,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 09:53:21",
                       "tp":  3974.285989285714
                   },
                   {
                       "alert_level":  "MEDIUM",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "INTRADAY_MED",
                       "entry":  3970.2646035714283,
                       "id":  4166,
                       "lots":  0.02,
                       "open_time":  "2025-11-05T07:50:10.052105",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3970.958892857143,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893587669,
                       "tier":  "",
                       "timestamp":  "2025-11-05 09:52:20",
                       "tp":  3963.2646035714283
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "FARMER",
                       "entry":  3970.2646035714283,
                       "id":  4167,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T07:50:10.218408",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  "TIME",
                       "sl":  3988.2646035714283,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893587676,
                       "tier":  "FARMER",
                       "timestamp":  "2025-11-05 09:52:20",
                       "tp":  3968.2646035714283
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3970.449489285714,
                       "id":  4165,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T07:49:39.667067",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3969.4044285714285,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893586618,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 09:51:49",
                       "tp":  3974.449489285714
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3970.8882642857143,
                       "id":  4164,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T07:49:09.227532",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3969.7704285714285,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893585357,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 09:51:18",
                       "tp":  3974.8882642857143
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3971.3655821428574,
                       "id":  4163,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T07:48:37.856208",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3970.0297142857144,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893582654,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 09:50:44",
                       "tp":  3975.3655821428574
                   },
                   {
                       "alert_level":  "MEDIUM",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "INTRADAY_MED",
                       "entry":  3970.9656642857144,
                       "id":  4161,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T07:48:01.427450",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3969.953071428571,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893580558,
                       "tier":  "",
                       "timestamp":  "2025-11-05 09:50:08",
                       "tp":  3977.9656642857144
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "FARMER",
                       "entry":  3970.9656642857144,
                       "id":  4162,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T07:48:04.672190",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3952.9656642857144,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893580623,
                       "tier":  "FARMER",
                       "timestamp":  "2025-11-05 09:50:08",
                       "tp":  3972.9656642857144
                   },
                   {
                       "alert_level":  "MEDIUM",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "INTRADAY_MED",
                       "entry":  3970.5594464285714,
                       "id":  4159,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T07:46:55.603950",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3969.522607142857,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893575354,
                       "tier":  "",
                       "timestamp":  "2025-11-05 09:48:55",
                       "tp":  3977.5594464285714
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "FARMER",
                       "entry":  3970.5594464285714,
                       "id":  4160,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T07:46:59.558211",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3952.5594464285714,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893575808,
                       "tier":  "FARMER",
                       "timestamp":  "2025-11-05 09:48:55",
                       "tp":  3972.5594464285714
                   },
                   {
                       "alert_level":  "MEDIUM",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "INTRADAY_MED",
                       "entry":  3969.6291392857142,
                       "id":  4157,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T07:45:13.608283",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3968.508821428571,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893570295,
                       "tier":  "",
                       "timestamp":  "2025-11-05 09:47:12",
                       "tp":  3976.6291392857142
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "FARMER",
                       "entry":  3969.6291392857142,
                       "id":  4158,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T07:45:15.401771",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3951.6291392857142,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893570464,
                       "tier":  "FARMER",
                       "timestamp":  "2025-11-05 09:47:12",
                       "tp":  3971.6291392857142
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3970.378,
                       "id":  4156,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T07:42:33.782764",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3968.779,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893563062,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 09:44:43",
                       "tp":  3974.378
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3970.577482142857,
                       "id":  4155,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T07:42:02.438809",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3968.958714285714,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893561531,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 09:44:11",
                       "tp":  3974.577482142857
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3969.5763785714284,
                       "id":  4154,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T07:41:30.618559",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3967.879857142857,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893559750,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 09:43:41",
                       "tp":  3973.5763785714284
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3970.5115464285714,
                       "id":  4153,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T07:41:00.189001",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3968.767142857143,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893557170,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 09:43:10",
                       "tp":  3974.5115464285714
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3968.9683785714287,
                       "id":  4152,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T07:39:07.610743",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3967.435857142857,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893549765,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 09:40:52",
                       "tp":  3972.9683785714287
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3969.592142857143,
                       "id":  4151,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T07:38:16.548647",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3968.151285714285,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893547188,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 09:40:15",
                       "tp":  3973.592142857143
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3970.1061,
                       "id":  4150,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T07:37:42.213524",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3968.667,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893545058,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 09:39:52",
                       "tp":  3974.1061
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3969.3935214285716,
                       "id":  4149,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T07:37:10.897107",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3968.019142857143,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893542598,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 09:39:12",
                       "tp":  3973.3935214285716
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3968.487814285714,
                       "id":  4148,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T07:36:33.978793",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3967.1834285714285,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893540554,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 09:38:41",
                       "tp":  3972.487814285714
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3969.1219107142856,
                       "id":  4147,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T07:36:02.803926",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3967.854571428571,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893538842,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 09:38:12",
                       "tp":  3973.1219107142856
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3968.879303571429,
                       "id":  4146,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T07:35:31.875416",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3967.636857142857,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893536970,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 09:37:42",
                       "tp":  3972.879303571429
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3969.7991785714285,
                       "id":  4145,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T07:34:30.775930",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3968.8078571428573,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893531509,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 09:36:39",
                       "tp":  3973.7991785714285
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3969.393092857143,
                       "id":  4144,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T07:33:59.319655",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3968.4052857142856,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893528547,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 09:36:09",
                       "tp":  3973.393092857143
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3969.0596964285714,
                       "id":  4143,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T07:33:28.659573",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3968.0471428571427,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893525516,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 09:35:38",
                       "tp":  3973.0596964285714
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3966.257675,
                       "id":  4142,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T07:32:27.516561",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3965.533,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893520552,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 09:34:37",
                       "tp":  3970.257675
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3966.995435714286,
                       "id":  4141,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T07:31:56.659147",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3966.1985714285715,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893518566,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 09:34:06",
                       "tp":  3970.995435714286
                   },
                   {
                       "alert_level":  "MEDIUM",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "INTRADAY_MED",
                       "entry":  3965.611142857143,
                       "id":  4139,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T07:25:22.061626",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3966.3507142857147,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893494949,
                       "tier":  "",
                       "timestamp":  "2025-11-05 09:27:31",
                       "tp":  3958.611142857143
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "FARMER",
                       "entry":  3965.611142857143,
                       "id":  4140,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T07:25:22.548335",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3983.611142857143,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893494972,
                       "tier":  "FARMER",
                       "timestamp":  "2025-11-05 09:27:31",
                       "tp":  3963.611142857143
                   },
                   {
                       "alert_level":  "LOW",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "INTRADAY_LOW",
                       "entry":  3966.8428321428573,
                       "id":  4137,
                       "lots":  0.03,
                       "open_time":  "2025-11-05T07:24:51.449251",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3967.287357142857,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893493176,
                       "tier":  "",
                       "timestamp":  "2025-11-05 09:27:01",
                       "tp":  3962.8428321428573
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "FARMER",
                       "entry":  3966.8428321428573,
                       "id":  4138,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T07:24:51.618488",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3984.8428321428573,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893493187,
                       "tier":  "FARMER",
                       "timestamp":  "2025-11-05 09:27:01",
                       "tp":  3964.8428321428573
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3966.256835714286,
                       "id":  4136,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T07:23:50.772656",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3965.3615714285716,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893488903,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 09:26:01",
                       "tp":  3970.256835714286
                   },
                   {
                       "alert_level":  "LOW",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "INTRADAY_LOW",
                       "entry":  3965.3178357142856,
                       "id":  4134,
                       "lots":  0.03,
                       "open_time":  "2025-11-05T07:22:19.229413",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3964.8592857142853,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893483204,
                       "tier":  "",
                       "timestamp":  "2025-11-05 09:24:29",
                       "tp":  3969.3178357142856
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "FARMER",
                       "entry":  3965.3178357142856,
                       "id":  4135,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T07:22:19.411245",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3947.3178357142856,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893483213,
                       "tier":  "FARMER",
                       "timestamp":  "2025-11-05 09:24:29",
                       "tp":  3967.3178357142856
                   },
                   {
                       "alert_level":  "LOW",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "INTRADAY_LOW",
                       "entry":  3965.4154857142858,
                       "id":  4132,
                       "lots":  0.02,
                       "open_time":  "2025-11-05T07:21:18.383748",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3964.817285714286,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893478868,
                       "tier":  "",
                       "timestamp":  "2025-11-05 09:23:28",
                       "tp":  3969.4154857142858
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "FARMER",
                       "entry":  3965.4154857142858,
                       "id":  4133,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T07:21:18.521224",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3947.4154857142858,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893478886,
                       "tier":  "FARMER",
                       "timestamp":  "2025-11-05 09:23:28",
                       "tp":  3967.4154857142858
                   },
                   {
                       "alert_level":  "LOW",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "INTRADAY_LOW",
                       "entry":  3964.629192857143,
                       "id":  4130,
                       "lots":  0.02,
                       "open_time":  "2025-11-05T07:20:16.676168",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3963.995142857143,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893471438,
                       "tier":  "",
                       "timestamp":  "2025-11-05 09:22:26",
                       "tp":  3968.629192857143
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "FARMER",
                       "entry":  3964.629192857143,
                       "id":  4131,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T07:20:17.594303",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3946.629192857143,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893471469,
                       "tier":  "FARMER",
                       "timestamp":  "2025-11-05 09:22:26",
                       "tp":  3966.629192857143
                   },
                   {
                       "alert_level":  "MEDIUM",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "INTRADAY_MED",
                       "entry":  3966.463339285714,
                       "id":  4128,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T07:17:14.135836",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3967.4448214285712,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893453154,
                       "tier":  "",
                       "timestamp":  "2025-11-05 09:19:24",
                       "tp":  3959.463339285714
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "FARMER",
                       "entry":  3966.463339285714,
                       "id":  4129,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T07:17:14.428060",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3984.463339285714,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893453172,
                       "tier":  "FARMER",
                       "timestamp":  "2025-11-05 09:19:24",
                       "tp":  3964.463339285714
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3967.038864285714,
                       "id":  4127,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T07:16:43.651514",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3965.6504285714286,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893450321,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 09:18:53",
                       "tp":  3971.038864285714
                   },
                   {
                       "alert_level":  "LOW",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "INTRADAY_LOW",
                       "entry":  3966.6067035714286,
                       "id":  4125,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T07:14:11.771905",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3967.3269285714287,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893435897,
                       "tier":  "",
                       "timestamp":  "2025-11-05 09:16:22",
                       "tp":  3962.6067035714286
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "FARMER",
                       "entry":  3966.6067035714286,
                       "id":  4126,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T07:14:12.048180",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3984.6067035714286,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893435919,
                       "tier":  "FARMER",
                       "timestamp":  "2025-11-05 09:16:22",
                       "tp":  3964.6067035714286
                   },
                   {
                       "alert_level":  "MEDIUM",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "INTRADAY_MED",
                       "entry":  3967.045275,
                       "id":  4123,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T07:09:33.255276",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3965.92075,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893416066,
                       "tier":  "",
                       "timestamp":  "2025-11-05 09:11:43",
                       "tp":  3974.045275
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "FARMER",
                       "entry":  3967.045275,
                       "id":  4124,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T07:09:33.392314",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3949.045275,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893416091,
                       "tier":  "FARMER",
                       "timestamp":  "2025-11-05 09:11:43",
                       "tp":  3969.045275
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "SWING_HIGH",
                       "entry":  3964.8380428571427,
                       "id":  4122,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T07:08:02.093017",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3966.0662857142856,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893406279,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 09:10:12",
                       "tp":  3960.8380428571427
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "SWING_HIGH",
                       "entry":  3964.762225,
                       "id":  4121,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T07:07:31.747115",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3965.9829999999997,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893404247,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 09:09:42",
                       "tp":  3960.762225
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "SWING_HIGH",
                       "entry":  3964.0111428571427,
                       "id":  4120,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T07:07:01.298758",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3965.3582857142856,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893401992,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 09:09:11",
                       "tp":  3960.0111428571427
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "SWING_HIGH",
                       "entry":  3963.8254357142855,
                       "id":  4119,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T07:06:30.671041",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3965.283571428571,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893399889,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 09:08:41",
                       "tp":  3959.8254357142855
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "SWING_HIGH",
                       "entry":  3964.8957714285716,
                       "id":  4118,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T07:05:29.978350",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3966.463142857143,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893394283,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 09:07:39",
                       "tp":  3960.8957714285716
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "SWING_HIGH",
                       "entry":  3965.114639285714,
                       "id":  4117,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T07:03:58.606879",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3966.5234285714287,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893387428,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 09:06:09",
                       "tp":  3961.114639285714
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "SWING_HIGH",
                       "entry":  3965.054271428571,
                       "id":  4116,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T07:03:28.175698",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3966.4781428571428,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893384911,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 09:05:38",
                       "tp":  3961.054271428571
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "SWING_HIGH",
                       "entry":  3965.1201035714284,
                       "id":  4115,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T07:02:57.824893",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3966.6738571428573,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893380986,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 09:05:08",
                       "tp":  3961.1201035714284
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "SWING_HIGH",
                       "entry":  3965.78445,
                       "id":  4114,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T07:01:57.098238",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3967.242,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893377352,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 09:04:06",
                       "tp":  3961.78445
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "SWING_HIGH",
                       "entry":  3966.2910821428572,
                       "id":  4113,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T07:01:26.713383",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3967.7227142857146,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893375535,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 09:03:36",
                       "tp":  3962.2910821428572
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "SWING_HIGH",
                       "entry":  3966.3672392857143,
                       "id":  4112,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T07:00:56.304529",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3967.792428571429,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893373125,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 09:03:06",
                       "tp":  3962.3672392857143
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "SWING_HIGH",
                       "entry":  3964.7856107142857,
                       "id":  4111,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T06:59:55.494913",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3966.0315714285716,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893367950,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 09:02:05",
                       "tp":  3960.7856107142857
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "SWING_HIGH",
                       "entry":  3965.7278035714285,
                       "id":  4110,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T06:59:25.057869",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3966.9248571428575,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893365438,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 09:01:34",
                       "tp":  3961.7278035714285
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "SWING_HIGH",
                       "entry":  3966.350378571429,
                       "id":  4109,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T06:58:54.698547",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3967.4828571428575,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893363542,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 09:01:04",
                       "tp":  3962.350378571429
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "SWING_HIGH",
                       "entry":  3965.0618535714284,
                       "id":  4108,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T06:57:53.640067",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3966.420857142857,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893358707,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 09:00:04",
                       "tp":  3961.0618535714284
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "SWING_HIGH",
                       "entry":  3966.697592857143,
                       "id":  4107,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T06:57:23.269513",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3967.862285714286,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893356741,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 08:59:33",
                       "tp":  3962.697592857143
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "SWING_HIGH",
                       "entry":  3966.4192,
                       "id":  4106,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T06:56:21.579927",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3967.723,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893353285,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 08:58:31",
                       "tp":  3962.4192
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "SWING_HIGH",
                       "entry":  3967.494728571429,
                       "id":  4105,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T06:55:14.658168",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3968.6538571428573,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893348431,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 08:57:24",
                       "tp":  3963.494728571429
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "SWING_HIGH",
                       "entry":  3967.4889857142857,
                       "id":  4104,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T06:54:43.877060",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3968.924571428571,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893346196,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 08:56:54",
                       "tp":  3963.4889857142857
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "SWING_HIGH",
                       "entry":  3967.816975,
                       "id":  4103,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T06:54:13.357770",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3969.294,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893344390,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 08:56:23",
                       "tp":  3963.816975
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "SWING_HIGH",
                       "entry":  3967.8490535714286,
                       "id":  4102,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T06:53:42.936180",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3969.322857142857,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893341171,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 08:55:53",
                       "tp":  3963.8490535714286
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "SWING_HIGH",
                       "entry":  3968.249967857143,
                       "id":  4101,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T06:53:12.604739",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3969.7272857142857,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893339132,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 08:55:22",
                       "tp":  3964.249967857143
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "SWING_HIGH",
                       "entry":  3968.238275,
                       "id":  4100,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T06:52:42.200492",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3969.744,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893336394,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 08:54:52",
                       "tp":  3964.238275
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "SWING_HIGH",
                       "entry":  3968.8453642857144,
                       "id":  4099,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T06:52:11.717617",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3970.3474285714287,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893334567,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 08:54:21",
                       "tp":  3964.8453642857144
                   },
                   {
                       "alert_level":  "LOW",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "INTRADAY_LOW",
                       "entry":  3967.7997285714287,
                       "id":  4097,
                       "lots":  0.02,
                       "open_time":  "2025-11-05T06:51:10.766708",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3967.0704285714282,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893329682,
                       "tier":  "",
                       "timestamp":  "2025-11-05 08:53:20",
                       "tp":  3971.7997285714287
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "FARMER",
                       "entry":  3967.7997285714287,
                       "id":  4098,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T06:51:10.932847",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  "TIME",
                       "sl":  3949.7997285714287,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893329692,
                       "tier":  "FARMER",
                       "timestamp":  "2025-11-05 08:53:20",
                       "tp":  3969.7997285714287
                   },
                   {
                       "alert_level":  "LOW",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "INTRADAY_LOW",
                       "entry":  3970.858810714286,
                       "id":  4095,
                       "lots":  0.02,
                       "open_time":  "2025-11-05T06:48:08.579711",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3970.274785714286,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893315194,
                       "tier":  "",
                       "timestamp":  "2025-11-05 08:50:18",
                       "tp":  3974.858810714286
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "FARMER",
                       "entry":  3970.858810714286,
                       "id":  4096,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T06:48:08.710467",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  "TIME",
                       "sl":  3952.858810714286,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893315205,
                       "tier":  "FARMER",
                       "timestamp":  "2025-11-05 08:50:18",
                       "tp":  3972.858810714286
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3972.7905357142854,
                       "id":  4094,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T06:40:50.883856",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3971.4565714285714,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893285964,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 08:43:00",
                       "tp":  3976.7905357142854
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3972.5398607142856,
                       "id":  4093,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T06:40:20.395453",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3971.233571428571,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893283931,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 08:42:30",
                       "tp":  3976.5398607142856
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3972.928867857143,
                       "id":  4092,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T06:39:49.707994",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3971.663285714286,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893281028,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 08:41:59",
                       "tp":  3976.928867857143
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3972.1387357142858,
                       "id":  4091,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T06:39:19.250316",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3970.7965714285715,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893277886,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 08:41:28",
                       "tp":  3976.1387357142858
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3971.807089285714,
                       "id":  4090,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T06:38:47.236835",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3970.4504285714283,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893274353,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 08:40:56",
                       "tp":  3975.807089285714
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3970.2348142857145,
                       "id":  4089,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T06:38:16.399787",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3968.9714285714285,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893271854,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 08:40:25",
                       "tp":  3974.2348142857145
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3969.8658857142855,
                       "id":  4088,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T06:37:45.410421",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3968.4765714285713,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893270177,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 08:39:55",
                       "tp":  3973.8658857142855
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "FARMER",
                       "entry":  3971.42185,
                       "id":  4087,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T06:36:44.495466",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3953.42185,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893265842,
                       "tier":  "FARMER",
                       "timestamp":  "2025-11-05 08:38:27",
                       "tp":  3973.42185
                   },
                   {
                       "alert_level":  "MEDIUM",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "INTRADAY_MED",
                       "entry":  3970.483642857143,
                       "id":  4085,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T06:36:05.991327",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3969.5027142857143,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893263051,
                       "tier":  "",
                       "timestamp":  "2025-11-05 08:38:15",
                       "tp":  3977.483642857143
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "FARMER",
                       "entry":  3970.483642857143,
                       "id":  4086,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T06:36:06.597572",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3952.483642857143,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893263077,
                       "tier":  "FARMER",
                       "timestamp":  "2025-11-05 08:38:15",
                       "tp":  3972.483642857143
                   },
                   {
                       "alert_level":  "MEDIUM",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "INTRADAY_MED",
                       "entry":  3970.8554357142857,
                       "id":  4083,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T06:35:34.609765",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3969.9119285714282,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893261044,
                       "tier":  "",
                       "timestamp":  "2025-11-05 08:37:44",
                       "tp":  3977.8554357142857
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "FARMER",
                       "entry":  3970.8554357142857,
                       "id":  4084,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T06:35:34.934851",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3952.8554357142857,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893261059,
                       "tier":  "FARMER",
                       "timestamp":  "2025-11-05 08:37:44",
                       "tp":  3972.8554357142857
                   },
                   {
                       "alert_level":  "MEDIUM",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "INTRADAY_MED",
                       "entry":  3972.0014642857145,
                       "id":  4081,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T06:35:03.781477",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3970.9950714285715,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893258748,
                       "tier":  "",
                       "timestamp":  "2025-11-05 08:37:13",
                       "tp":  3979.0014642857145
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "FARMER",
                       "entry":  3972.0014642857145,
                       "id":  4082,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T06:35:04.069270",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  "TIME",
                       "sl":  3954.0014642857145,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893258756,
                       "tier":  "FARMER",
                       "timestamp":  "2025-11-05 08:37:13",
                       "tp":  3974.0014642857145
                   },
                   {
                       "alert_level":  "MEDIUM",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "INTRADAY_MED",
                       "entry":  3972.4873214285717,
                       "id":  4079,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T06:34:32.763019",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3971.5163571428575,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893256519,
                       "tier":  "",
                       "timestamp":  "2025-11-05 08:36:43",
                       "tp":  3979.4873214285717
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "FARMER",
                       "entry":  3972.4873214285717,
                       "id":  4080,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T06:34:33.193598",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  "TIME",
                       "sl":  3954.4873214285717,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893256534,
                       "tier":  "FARMER",
                       "timestamp":  "2025-11-05 08:36:43",
                       "tp":  3974.4873214285717
                   },
                   {
                       "alert_level":  "MEDIUM",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "INTRADAY_MED",
                       "entry":  3972.174728571428,
                       "id":  4077,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T06:34:01.325008",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3971.2221428571424,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893253857,
                       "tier":  "",
                       "timestamp":  "2025-11-05 08:36:10",
                       "tp":  3979.174728571428
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "FARMER",
                       "entry":  3972.174728571428,
                       "id":  4078,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T06:34:02.116153",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  "TIME",
                       "sl":  3954.174728571428,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893253894,
                       "tier":  "FARMER",
                       "timestamp":  "2025-11-05 08:36:10",
                       "tp":  3974.174728571428
                   },
                   {
                       "alert_level":  "MEDIUM",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "INTRADAY_MED",
                       "entry":  3971.5837464285714,
                       "id":  4075,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T06:33:29.588316",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3970.661607142857,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893250667,
                       "tier":  "",
                       "timestamp":  "2025-11-05 08:35:38",
                       "tp":  3978.5837464285714
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "FARMER",
                       "entry":  3971.5837464285714,
                       "id":  4076,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T06:33:30.194379",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3953.5837464285714,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893250705,
                       "tier":  "FARMER",
                       "timestamp":  "2025-11-05 08:35:38",
                       "tp":  3973.5837464285714
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3971.524432142857,
                       "id":  4074,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T06:32:58.666094",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3970.235714285714,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893248930,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 08:35:07",
                       "tp":  3975.524432142857
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3970.0937035714283,
                       "id":  4073,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T06:31:55.714477",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3968.957857142857,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893242798,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 08:34:06",
                       "tp":  3974.0937035714283
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3969.662428571429,
                       "id":  4072,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T06:31:24.743783",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3968.5378571428573,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893240309,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 08:33:34",
                       "tp":  3973.662428571429
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3968.142057142857,
                       "id":  4071,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T06:26:18.767584",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3966.622714285714,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893216653,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 08:28:27",
                       "tp":  3972.142057142857
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3968.6761428571426,
                       "id":  4070,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T06:25:47.871929",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3967.1122857142855,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893214874,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 08:27:56",
                       "tp":  3972.6761428571426
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3968.8524428571427,
                       "id":  4069,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T06:25:17.318597",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3967.1122857142855,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893213373,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 08:27:27",
                       "tp":  3972.8524428571427
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3969.0634785714287,
                       "id":  4068,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T06:24:46.798864",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3967.3218571428574,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893211450,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 08:26:55",
                       "tp":  3973.0634785714287
                   },
                   {
                       "alert_level":  "MEDIUM",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "INTRADAY_MED",
                       "entry":  3969.3314107142855,
                       "id":  4066,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T06:24:15.346539",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3970.682678571429,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893209175,
                       "tier":  "",
                       "timestamp":  "2025-11-05 08:26:24",
                       "tp":  3962.3314107142855
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  -1,
                       "engine":  "FARMER",
                       "entry":  3969.3314107142855,
                       "id":  4067,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T06:24:15.990755",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3987.3314107142855,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893209316,
                       "tier":  "FARMER",
                       "timestamp":  "2025-11-05 08:26:24",
                       "tp":  3967.3314107142855
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3975.1323231554456,
                       "id":  4065,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T06:23:43.612662",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  "TIME",
                       "sl":  3741.2140737821856,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893207338,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 08:25:53",
                       "tp":  3979.1323231554456
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3974.55204623674,
                       "id":  4064,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T06:23:12.875373",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  "TIME",
                       "sl":  3736.0121505304064,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893205323,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 08:25:22",
                       "tp":  3978.55204623674
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3975.183983425558,
                       "id":  4063,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T06:22:42.200317",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  "TIME",
                       "sl":  3732.464662977682,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893201912,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 08:24:51",
                       "tp":  3979.183983425558
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3974.826911148865,
                       "id":  4062,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T06:22:11.234269",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  "TIME",
                       "sl":  3723.0085540454097,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893199403,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 08:24:20",
                       "tp":  3978.826911148865
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3973.535351982484,
                       "id":  4061,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T06:21:39.982909",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3716.122920700646,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893196890,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 08:23:50",
                       "tp":  3977.535351982484
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3972.898167965978,
                       "id":  4060,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T06:21:09.410107",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3710.5732813608856,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893194397,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 08:23:19",
                       "tp":  3976.898167965978
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3973.2141894109477,
                       "id":  4059,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T06:20:38.965449",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3706.9114235620923,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893191978,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 08:22:48",
                       "tp":  3977.2141894109477
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3973.1257132337078,
                       "id":  4058,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T06:20:07.716305",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3701.1844706516913,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893189527,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 08:22:16",
                       "tp":  3977.1257132337078
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3975.281380925958,
                       "id":  4057,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T06:19:35.904952",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  "TIME",
                       "sl":  3698.3107629616893,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893186063,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 08:21:45",
                       "tp":  3979.281380925958
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3972.7976310340878,
                       "id":  4056,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T06:19:04.339518",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3691.511758636488,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893183384,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 08:21:11",
                       "tp":  3976.7976310340878
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3972.05695915713,
                       "id":  4055,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T06:18:30.113024",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3686.821633714788,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893180115,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 08:20:38",
                       "tp":  3976.05695915713
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3973.5407549878855,
                       "id":  4054,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T06:17:39.486466",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3683.885800484591,
                       "status":  "CLOSED",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893175805,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 08:19:39",
                       "tp":  3977.5407549878855
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3972.1356068544724,
                       "id":  4053,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T06:15:56.970819",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3736.975725821106,
                       "status":  "OPEN",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893167151,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 08:18:05",
                       "tp":  3976.1356068544724
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3971.098630039124,
                       "id":  4052,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T06:15:24.538466",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3733.6417984350223,
                       "status":  "OPEN",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893164345,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 08:17:33",
                       "tp":  3975.098630039124
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3971.3026897133477,
                       "id":  4051,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T06:14:52.741873",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3729.374411466086,
                       "status":  "OPEN",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893160705,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 08:17:00",
                       "tp":  3975.3026897133477
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3970.9829723175258,
                       "id":  4050,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T06:14:19.877598",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3723.713107298986,
                       "status":  "OPEN",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893158581,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 08:16:28",
                       "tp":  3974.9829723175258
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3970.1936568396954,
                       "id":  4049,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T06:13:48.744798",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3721.255726412168,
                       "status":  "OPEN",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893155517,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 08:15:56",
                       "tp":  3974.1936568396954
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3971.062271645164,
                       "id":  4048,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T06:13:16.810714",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3717.2611341934353,
                       "status":  "OPEN",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893153452,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 08:15:26",
                       "tp":  3975.062271645164
                   },
                   {
                       "alert_level":  "HIGH",
                       "campaign_id":  null,
                       "close_price":  null,
                       "close_time":  null,
                       "direction":  1,
                       "engine":  "SWING_HIGH",
                       "entry":  3971.2046765244554,
                       "id":  4047,
                       "lots":  0.01,
                       "open_time":  "2025-11-05T06:12:45.310440",
                       "pnl":  null,
                       "pnl_r":  null,
                       "reason":  null,
                       "sl":  3710.621939021795,
                       "status":  "OPEN",
                       "symbol":  "XAUUSDm",
                       "ticket":  1893150743,
                       "tier":  "TIER1",
                       "timestamp":  "2025-11-05 08:14:54",
                       "tp":  3975.2046765244554
                   }
               ]
}
PS C:\Users\ndlal\getrichfrbot> $resp = Invoke-RestMethod "http://localhost:5000/api/recent_trades?hours=24&limit=2000"
PS C:\Users\ndlal\getrichfrbot>
PS C:\Users\ndlal\getrichfrbot> $winners = $resp.trades |
>>   Where-Object { $_.status -eq 'CLOSED' -and $_.close_price } |
>>   ForEach-Object {
>>     $entry = [double]$_.entry
>>     $close = [double]$_.close_price
>>     $dir   = [int]$_.direction
>>     $profit_points = if ($dir -eq 1) { $close - $entry } else { $entry - $close }
>>     $_ | Add-Member -NotePropertyName profit_points -NotePropertyValue $profit_points -PassThru
>>   } |
>>   Where-Object { $_.profit_points -gt 0 }
PS C:\Users\ndlal\getrichfrbot>
PS C:\Users\ndlal\getrichfrbot> $winners |
>>   Select-Object timestamp, symbol, engine, direction, entry, close_price, profit_points, ticket |
>>   Format-Table -AutoSize
PS C:\Users\ndlal\getrichfrbot> $resp.trades |
>>   Where-Object { $_.status -eq 'CLOSED' -and $_.pnl -gt 0 } |
>>   Select-Object timestamp, symbol, engine, direction, entry, close_price, pnl, pnl_r, ticket |
>>   Format-Table -AutoSize
PS C:\Users\ndlal\getrichfrbot> $winners |
>>   Select-Object timestamp, symbol, engine, direction, entry, close_price, profit
PS C:\Users\ndlal\getrichfrbot> $resp = Invoke-RestMethod "http://localhost:5000/api/recent_trades?hours=24&limit=2000"
PS C:\Users\ndlal\getrichfrbot>
PS C:\Users\ndlal\getrichfrbot> $closed = $resp.trades | Where-Object { $_.status -eq 'CLOSED' }
PS C:\Users\ndlal\getrichfrbot>
PS C:\Users\ndlal\getrichfrbot> $winners = $closed | ForEach-Object {
>>   $entry = [double]$_.entry
>>   $dir   = [int]$_.direction
>>   # effective close: prefer close_price, else TP/SL if present
>>   $closeEff = if ($_.close_price) { [double]$_.close_price }
>>               elseif ($_.tp)      { [double]$_.tp }
>>               elseif ($_.sl)      { [double]$_.sl }
>>               else { $null }
>>
>>   if ($null -ne $closeEff) {
>>     $profit_points = if ($dir -eq 1) { $closeEff - $entry } else { $entry - $closeEff }
>>     $_ | Add-Member -NotePropertyName profit_points -NotePropertyValue $profit_points -PassThru
>>   }
>> } | Where-Object { $_.profit_points -gt 0 }
PS C:\Users\ndlal\getrichfrbot>
PS C:\Users\ndlal\getrichfrbot> $winners |
>>   Select-Object timestamp, symbol, engine, direction, entry, close_price, tp, sl, profit_points, ticket |
>>   Format-Table -AutoSize

timestamp           symbol  engine       direction              entry close_price                 tp                 sl profit_points     ticket
---------           ------  ------       ---------              ----- -----------                 --                 -- -------------     ------
2025-11-05 11:59:44 XAUUSDm SWING_HIGH           1  3971,702857142857              3975,702857142857  3971,134714285714             4 1894333116
2025-11-05 11:59:12 XAUUSDm SWING_HIGH           1        3971,642575                    3975,642575           3971,004             4 1894331627
2025-11-05 11:58:42 XAUUSDm SWING_HIGH           1 3971,1273607142857             3975,1273607142857 3970,5385714285712             4 1894329689
2025-11-05 11:57:41 XAUUSDm SWING_HIGH          -1 3970,6419428571426             3966,6419428571426 3971,3002857142856             4 1894326394
2025-11-05 11:51:04 XAUUSDm SWING_HIGH          -1  3970,074507142857              3966,074507142857  3971,037714285714             4 1894295112
2025-11-05 11:49:33 XAUUSDm SWING_HIGH          -1 3970,3144964285716             3966,3144964285716  3971,278142857143             4 1894288949
2025-11-05 11:47:01 XAUUSDm SWING_HIGH          -1 3969,1045107142854             3965,1045107142854  3969,903571428571             4 1894275593
2025-11-05 11:40:22 XAUUSDm SWING_HIGH          -1  3970,251021428571              3966,251021428571 3972,3821428571428             4 1894245071
2025-11-05 11:39:51 XAUUSDm SWING_HIGH          -1 3969,6093214285715             3965,6093214285715  3971,646142857143             4 1894241689
2025-11-05 11:39:20 XAUUSDm SWING_HIGH          -1 3967,8625821428573             3963,8625821428573  3969,642714285714             4 1894238494
2025-11-05 11:38:50 XAUUSDm SWING_HIGH          -1 3968,0893892857143             3964,0893892857143 3969,8364285714288             4 1894236302
2025-11-05 11:38:19 XAUUSDm SWING_HIGH          -1 3967,6788607142853             3963,6788607142853 3969,3655714285715             4 1894234413
2025-11-05 11:37:50 XAUUSDm SWING_HIGH          -1 3967,7350607142857             3963,7350607142857 3969,4135714285712             4 1894231964
2025-11-05 11:37:15 XAUUSDm SWING_HIGH          -1 3968,0448071428573             3964,0448071428573 3969,6927142857144             4 1894228797
2025-11-05 11:36:44 XAUUSDm SWING_HIGH          -1 3969,0379107142858             3965,0379107142858 3970,6405714285715             4 1894225289
2025-11-05 11:36:14 XAUUSDm SWING_HIGH          -1  3969,049039285714              3965,049039285714 3970,6874285714284             4 1894223112
2025-11-05 11:35:31 XAUUSDm SWING_HIGH          -1  3969,109346428572              3965,109346428572  3970,981142857143             4 1894220914
2025-11-05 11:16:37 XAUUSDm SWING_HIGH          -1         3972,90385                     3968,90385           3974,222             4 1894102564
2025-11-05 11:11:06 XAUUSDm SWING_HIGH          -1  3977,290503571429              3973,290503571429  3978,130857142857             4 1894063514
2025-11-05 11:02:13 XAUUSDm SWING_HIGH          -1        3978,319075                    3974,319075           3979,505             4 1893990149
2025-11-05 11:01:42 XAUUSDm SWING_HIGH          -1 3978,5380571428573             3974,5380571428573 3979,7657142857142             4 1893987892
2025-11-05 11:01:13 XAUUSDm SWING_HIGH          -1  3978,101532142857              3974,101532142857  3979,309714285714             4 1893985901
2025-11-05 11:00:42 XAUUSDm SWING_HIGH          -1  3977,992357142857              3973,992357142857 3979,2077142857142             4 1893983139
2025-11-05 10:59:41 XAUUSDm SWING_HIGH          -1 3980,0518178571433             3976,0518178571433 3981,0842857142857             4 1893974499
2025-11-05 10:52:59 XAUUSDm INTRADAY_MED         1  3981,262242857143              3988,262242857143 3980,6347142857144             7 1893939603
2025-11-05 10:51:57 XAUUSDm SWING_HIGH          -1  3980,884128571429              3976,884128571429  3981,739857142857             4 1893934332
2025-11-05 10:50:43 XAUUSDm SWING_HIGH          -1  3980,279582142857              3976,279582142857 3981,1987142857142             4 1893928704
2025-11-05 10:43:16 XAUUSDm INTRADAY_MED        -1 3982,8082464285712             3975,8082464285712 3983,6066071428572             7 1893894289
2025-11-05 10:42:45 XAUUSDm SWING_HIGH           1 3984,2207285714285             3988,2207285714285 3983,3298571428572             4 1893891943
2025-11-05 10:42:15 XAUUSDm SWING_HIGH           1 3984,4633357142857             3988,4633357142857 3983,5065714285715             4 1893889872
2025-11-05 10:41:44 XAUUSDm SWING_HIGH           1 3984,4918071428574             3988,4918071428574 3983,4747142857145             4 1893887980
2025-11-05 10:41:14 XAUUSDm SWING_HIGH           1 3984,4165892857145             3988,4165892857145 3983,3674285714287             4 1893885526
2025-11-05 10:39:53 XAUUSDm SWING_HIGH           1 3984,7924392857144             3988,7924392857144 3983,6264285714287             4 1893878491
2025-11-05 10:39:23 XAUUSDm SWING_HIGH           1 3984,8603035714286             3988,8603035714286 3983,6588571428574             4 1893876080
2025-11-05 10:38:53 XAUUSDm SWING_HIGH           1  3984,958207142857              3988,958207142857  3983,555714285714             4 1893872631
2025-11-05 10:38:22 XAUUSDm SWING_HIGH           1 3984,8227464285715             3988,8227464285715  3983,398142857143             4 1893869719
2025-11-05 10:37:22 XAUUSDm INTRADAY_LOW        -1  3982,824964285714              3978,824964285714  3983,497714285714             4 1893864815
2025-11-05 10:31:49 XAUUSDm INTRADAY_MED         1 3981,2576357142857             3988,2576357142857 3980,1529285714287             7 1893833067
2025-11-05 10:30:48 XAUUSDm SWING_HIGH          -1  3980,139842857143              3976,139842857143 3981,5402857142853             4 1893828159
2025-11-05 10:30:18 XAUUSDm SWING_HIGH          -1  3980,548760714286              3976,548760714286 3982,0345714285713             4 1893825577
2025-11-05 10:29:47 XAUUSDm SWING_HIGH          -1 3979,5524571428573             3975,5524571428573 3981,0097142857144             4 1893821286
2025-11-05 10:29:17 XAUUSDm SWING_HIGH          -1 3978,9951535714285             3974,9951535714285 3980,3828571428567             4 1893818402
2025-11-05 10:28:47 XAUUSDm SWING_HIGH          -1 3980,0591857142854             3976,0591857142854  3981,445571428571             4 1893815386
2025-11-05 10:28:16 XAUUSDm SWING_HIGH          -1  3979,305017857143              3975,305017857143 3980,7392857142854             4 1893811630
2025-11-05 10:27:46 XAUUSDm INTRADAY_LOW         1 3979,2713392857145             3983,2713392857145 3978,4662142857146             4 1893808460
2025-11-05 10:21:37 XAUUSDm INTRADAY_LOW         1  3980,266628571429              3984,266628571429 3979,5184285714286             4 1893770609
2025-11-05 10:19:05 XAUUSDm SWING_HIGH           1 3983,9891714285714             3987,9891714285714  3982,342142857143             4 1893756437
2025-11-05 10:12:34 XAUUSDm INTRADAY_MED         1 3984,4834464285714             3991,4834464285714 3981,8656071428572             7 1893716809
2025-11-05 10:12:34 XAUUSDm FARMER               1 3984,4834464285714             3986,4834464285714 3966,4834464285714             2 1893716855
2025-11-05 10:12:04 XAUUSDm INTRADAY_MED        -1         3981,66545                     3974,66545          3984,0385             7 1893713574
2025-11-05 10:12:04 XAUUSDm FARMER              -1         3981,66545                     3979,66545         3999,66545             2 1893713583
2025-11-05 10:11:33 XAUUSDm SWING_HIGH           1 3982,8184107142856             3986,8184107142856 3979,7265714285713             4 1893710154
2025-11-05 10:10:00 XAUUSDm SWING_HIGH           1  3986,436603571429              3990,436603571429 3983,6648571428573             4 1893700050
2025-11-05 10:09:31 XAUUSDm SWING_HIGH           1 3985,5940571428573             3989,5940571428573 3982,9267142857143             4 1893695507
2025-11-05 10:08:54 XAUUSDm SWING_HIGH           1        3986,150425                    3990,150425            3983,55             4 1893692255
2025-11-05 10:07:51 XAUUSDm SWING_HIGH           1 3984,0667714285714             3988,0667714285714  3981,616142857143             4 1893683036
2025-11-05 10:07:19 XAUUSDm SWING_HIGH           1 3985,4036107142856             3989,4036107142856 3983,1235714285713             4 1893678665
2025-11-05 10:06:47 XAUUSDm SWING_HIGH           1  3984,514682142857              3988,514682142857  3982,354714285714             4 1893673876
2025-11-05 10:06:17 XAUUSDm SWING_HIGH           1 3982,2249642857146             3986,2249642857146 3980,3404285714287             4 1893668999
2025-11-05 10:05:09 XAUUSDm SWING_HIGH           1 3977,0433357142856             3981,0433357142856 3975,7175714285713             4 1893652676
2025-11-05 10:04:34 XAUUSDm INTRADAY_MED         1  3974,748410714286              3981,748410714286 3973,9296785714287             7 1893647442
2025-11-05 10:04:34 XAUUSDm FARMER               1  3974,748410714286              3976,748410714286  3956,748410714286             2 1893647475
2025-11-05 10:04:06 XAUUSDm INTRADAY_MED        -1 3974,2497285714285             3967,2497285714285 3975,0641428571425             7 1893644414
2025-11-05 10:04:06 XAUUSDm FARMER              -1 3974,2497285714285             3972,2497285714285 3992,2497285714285             2 1893644465
2025-11-05 10:03:36 XAUUSDm SWING_HIGH           1  3973,623085714286              3977,623085714286 3972,4305714285715             4 1893640962
2025-11-05 10:03:06 XAUUSDm SWING_HIGH           1  3974,293985714286              3978,293985714286 3973,1465714285714             4 1893638295
2025-11-05 10:02:35 XAUUSDm SWING_HIGH           1  3975,060457142857              3979,060457142857 3973,9757142857143             4 1893635764
2025-11-05 10:02:06 XAUUSDm SWING_HIGH           1  3975,188160714286              3979,188160714286 3974,0745714285713             4 1893633648
2025-11-05 10:01:33 XAUUSDm SWING_HIGH           1 3975,0888178571427             3979,0888178571427 3973,9072857142855             4 1893630582
2025-11-05 09:58:59 XAUUSDm SWING_HIGH           1        3973,421375                    3977,421375           3972,422             4 1893614700
2025-11-05 09:58:29 XAUUSDm SWING_HIGH           1          3973,8235                      3977,8235           3972,819             4 1893612848
2025-11-05 09:57:58 XAUUSDm SWING_HIGH           1          3973,9328                      3977,9328           3972,875             4 1893610292
2025-11-05 09:57:26 XAUUSDm SWING_HIGH           1  3972,685785714286              3976,685785714286 3971,7515714285714             4 1893605886
2025-11-05 09:56:56 XAUUSDm SWING_HIGH           1 3972,0549892857143             3976,0549892857143 3971,1534285714283             4 1893602296
2025-11-05 09:56:25 XAUUSDm INTRADAY_MED         1  3971,648603571429              3978,648603571429  3970,947892857143             7 1893600183
2025-11-05 09:56:25 XAUUSDm FARMER               1  3971,648603571429              3973,648603571429  3953,648603571429             2 1893600286
2025-11-05 09:55:54 XAUUSDm SWING_HIGH           1 3970,1754071428572             3974,1754071428572 3969,3797142857143             4 1893598340
2025-11-05 09:54:21 XAUUSDm INTRADAY_MED         1 3970,4757821428575             3977,4757821428575  3969,862535714286             7 1893592991
2025-11-05 09:54:21 XAUUSDm FARMER               1 3970,4757821428575             3972,4757821428575 3952,4757821428575             2 1893593010
2025-11-05 09:53:51 XAUUSDm INTRADAY_MED         1 3971,0412535714286             3978,0412535714286  3970,413392857143             7 1893591635
2025-11-05 09:53:51 XAUUSDm FARMER               1 3971,0412535714286             3973,0412535714286 3953,0412535714286             2 1893591650
2025-11-05 09:53:21 XAUUSDm SWING_HIGH           1  3970,285989285714              3974,285989285714 3969,5074285714286             4 1893590339
2025-11-05 09:52:20 XAUUSDm INTRADAY_MED        -1 3970,2646035714283             3963,2646035714283  3970,958892857143             7 1893587669
2025-11-05 09:52:20 XAUUSDm FARMER              -1 3970,2646035714283             3968,2646035714283 3988,2646035714283             2 1893587676
2025-11-05 09:51:49 XAUUSDm SWING_HIGH           1  3970,449489285714              3974,449489285714 3969,4044285714285             4 1893586618
2025-11-05 09:51:18 XAUUSDm SWING_HIGH           1 3970,8882642857143             3974,8882642857143 3969,7704285714285             4 1893585357
2025-11-05 09:50:44 XAUUSDm SWING_HIGH           1 3971,3655821428574             3975,3655821428574 3970,0297142857144             4 1893582654
2025-11-05 09:50:08 XAUUSDm INTRADAY_MED         1 3970,9656642857144             3977,9656642857144  3969,953071428571             7 1893580558
2025-11-05 09:50:08 XAUUSDm FARMER               1 3970,9656642857144             3972,9656642857144 3952,9656642857144             2 1893580623
2025-11-05 09:48:55 XAUUSDm INTRADAY_MED         1 3970,5594464285714             3977,5594464285714  3969,522607142857             7 1893575354
2025-11-05 09:48:55 XAUUSDm FARMER               1 3970,5594464285714             3972,5594464285714 3952,5594464285714             2 1893575808
2025-11-05 09:47:12 XAUUSDm INTRADAY_MED         1 3969,6291392857142             3976,6291392857142  3968,508821428571             7 1893570295
2025-11-05 09:47:12 XAUUSDm FARMER               1 3969,6291392857142             3971,6291392857142 3951,6291392857142             2 1893570464
2025-11-05 09:44:43 XAUUSDm SWING_HIGH           1           3970,378                       3974,378           3968,779             4 1893563062
2025-11-05 09:44:11 XAUUSDm SWING_HIGH           1  3970,577482142857              3974,577482142857  3968,958714285714             4 1893561531
2025-11-05 09:43:41 XAUUSDm SWING_HIGH           1 3969,5763785714284             3973,5763785714284  3967,879857142857             4 1893559750
2025-11-05 09:43:10 XAUUSDm SWING_HIGH           1 3970,5115464285714             3974,5115464285714  3968,767142857143             4 1893557170
2025-11-05 09:40:52 XAUUSDm SWING_HIGH           1 3968,9683785714287             3972,9683785714287  3967,435857142857             4 1893549765
2025-11-05 09:40:15 XAUUSDm SWING_HIGH           1  3969,592142857143              3973,592142857143  3968,151285714285             4 1893547188
2025-11-05 09:39:52 XAUUSDm SWING_HIGH           1          3970,1061                      3974,1061           3968,667             4 1893545058
2025-11-05 09:39:12 XAUUSDm SWING_HIGH           1 3969,3935214285716             3973,3935214285716  3968,019142857143             4 1893542598
2025-11-05 09:38:41 XAUUSDm SWING_HIGH           1  3968,487814285714              3972,487814285714 3967,1834285714285             4 1893540554
2025-11-05 09:38:12 XAUUSDm SWING_HIGH           1 3969,1219107142856             3973,1219107142856  3967,854571428571             4 1893538842
2025-11-05 09:37:42 XAUUSDm SWING_HIGH           1  3968,879303571429              3972,879303571429  3967,636857142857             4 1893536970
2025-11-05 09:36:39 XAUUSDm SWING_HIGH           1 3969,7991785714285             3973,7991785714285 3968,8078571428573             4 1893531509
2025-11-05 09:36:09 XAUUSDm SWING_HIGH           1  3969,393092857143              3973,393092857143 3968,4052857142856             4 1893528547
2025-11-05 09:35:38 XAUUSDm SWING_HIGH           1 3969,0596964285714             3973,0596964285714 3968,0471428571427             4 1893525516
2025-11-05 09:34:37 XAUUSDm SWING_HIGH           1        3966,257675                    3970,257675           3965,533             4 1893520552
2025-11-05 09:34:06 XAUUSDm SWING_HIGH           1  3966,995435714286              3970,995435714286 3966,1985714285715             4 1893518566
2025-11-05 09:27:31 XAUUSDm INTRADAY_MED        -1  3965,611142857143              3958,611142857143 3966,3507142857147             7 1893494949
2025-11-05 09:27:31 XAUUSDm FARMER              -1  3965,611142857143              3963,611142857143  3983,611142857143             2 1893494972
2025-11-05 09:27:01 XAUUSDm INTRADAY_LOW        -1 3966,8428321428573             3962,8428321428573  3967,287357142857             4 1893493176
2025-11-05 09:27:01 XAUUSDm FARMER              -1 3966,8428321428573             3964,8428321428573 3984,8428321428573             2 1893493187
2025-11-05 09:26:01 XAUUSDm SWING_HIGH           1  3966,256835714286              3970,256835714286 3965,3615714285716             4 1893488903
2025-11-05 09:24:29 XAUUSDm INTRADAY_LOW         1 3965,3178357142856             3969,3178357142856 3964,8592857142853             4 1893483204
2025-11-05 09:24:29 XAUUSDm FARMER               1 3965,3178357142856             3967,3178357142856 3947,3178357142856             2 1893483213
2025-11-05 09:23:28 XAUUSDm INTRADAY_LOW         1 3965,4154857142858             3969,4154857142858  3964,817285714286             4 1893478868
2025-11-05 09:23:28 XAUUSDm FARMER               1 3965,4154857142858             3967,4154857142858 3947,4154857142858             2 1893478886
2025-11-05 09:22:26 XAUUSDm INTRADAY_LOW         1  3964,629192857143              3968,629192857143  3963,995142857143             4 1893471438
2025-11-05 09:22:26 XAUUSDm FARMER               1  3964,629192857143              3966,629192857143  3946,629192857143             2 1893471469
2025-11-05 09:19:24 XAUUSDm INTRADAY_MED        -1  3966,463339285714              3959,463339285714 3967,4448214285712             7 1893453154
2025-11-05 09:19:24 XAUUSDm FARMER              -1  3966,463339285714              3964,463339285714  3984,463339285714             2 1893453172
2025-11-05 09:18:53 XAUUSDm SWING_HIGH           1  3967,038864285714              3971,038864285714 3965,6504285714286             4 1893450321
2025-11-05 09:16:22 XAUUSDm INTRADAY_LOW        -1 3966,6067035714286             3962,6067035714286 3967,3269285714287             4 1893435897
2025-11-05 09:16:22 XAUUSDm FARMER              -1 3966,6067035714286             3964,6067035714286 3984,6067035714286             2 1893435919
2025-11-05 09:11:43 XAUUSDm INTRADAY_MED         1        3967,045275                    3974,045275         3965,92075             7 1893416066
2025-11-05 09:11:43 XAUUSDm FARMER               1        3967,045275                    3969,045275        3949,045275             2 1893416091
2025-11-05 09:10:12 XAUUSDm SWING_HIGH          -1 3964,8380428571427             3960,8380428571427 3966,0662857142856             4 1893406279
2025-11-05 09:09:42 XAUUSDm SWING_HIGH          -1        3964,762225                    3960,762225 3965,9829999999997             4 1893404247
2025-11-05 09:09:11 XAUUSDm SWING_HIGH          -1 3964,0111428571427             3960,0111428571427 3965,3582857142856             4 1893401992
2025-11-05 09:08:41 XAUUSDm SWING_HIGH          -1 3963,8254357142855             3959,8254357142855  3965,283571428571             4 1893399889
2025-11-05 09:07:39 XAUUSDm SWING_HIGH          -1 3964,8957714285716             3960,8957714285716  3966,463142857143             4 1893394283
2025-11-05 09:06:09 XAUUSDm SWING_HIGH          -1  3965,114639285714              3961,114639285714 3966,5234285714287             4 1893387428
2025-11-05 09:05:38 XAUUSDm SWING_HIGH          -1  3965,054271428571              3961,054271428571 3966,4781428571428             4 1893384911
2025-11-05 09:05:08 XAUUSDm SWING_HIGH          -1 3965,1201035714284             3961,1201035714284 3966,6738571428573             4 1893380986
2025-11-05 09:04:06 XAUUSDm SWING_HIGH          -1         3965,78445                     3961,78445           3967,242             4 1893377352
2025-11-05 09:03:36 XAUUSDm SWING_HIGH          -1 3966,2910821428572             3962,2910821428572 3967,7227142857146             4 1893375535
2025-11-05 09:03:06 XAUUSDm SWING_HIGH          -1 3966,3672392857143             3962,3672392857143  3967,792428571429             4 1893373125
2025-11-05 09:02:05 XAUUSDm SWING_HIGH          -1 3964,7856107142857             3960,7856107142857 3966,0315714285716             4 1893367950
2025-11-05 09:01:34 XAUUSDm SWING_HIGH          -1 3965,7278035714285             3961,7278035714285 3966,9248571428575             4 1893365438
2025-11-05 09:01:04 XAUUSDm SWING_HIGH          -1  3966,350378571429              3962,350378571429 3967,4828571428575             4 1893363542
2025-11-05 09:00:04 XAUUSDm SWING_HIGH          -1 3965,0618535714284             3961,0618535714284  3966,420857142857             4 1893358707
2025-11-05 08:59:33 XAUUSDm SWING_HIGH          -1  3966,697592857143              3962,697592857143  3967,862285714286             4 1893356741
2025-11-05 08:58:31 XAUUSDm SWING_HIGH          -1          3966,4192                      3962,4192           3967,723             4 1893353285
2025-11-05 08:57:24 XAUUSDm SWING_HIGH          -1  3967,494728571429              3963,494728571429 3968,6538571428573             4 1893348431
2025-11-05 08:56:54 XAUUSDm SWING_HIGH          -1 3967,4889857142857             3963,4889857142857  3968,924571428571             4 1893346196
2025-11-05 08:56:23 XAUUSDm SWING_HIGH          -1        3967,816975                    3963,816975           3969,294             4 1893344390
2025-11-05 08:55:53 XAUUSDm SWING_HIGH          -1 3967,8490535714286             3963,8490535714286  3969,322857142857             4 1893341171
2025-11-05 08:55:22 XAUUSDm SWING_HIGH          -1  3968,249967857143              3964,249967857143 3969,7272857142857             4 1893339132
2025-11-05 08:54:52 XAUUSDm SWING_HIGH          -1        3968,238275                    3964,238275           3969,744             4 1893336394
2025-11-05 08:54:21 XAUUSDm SWING_HIGH          -1 3968,8453642857144             3964,8453642857144 3970,3474285714287             4 1893334567
2025-11-05 08:53:20 XAUUSDm INTRADAY_LOW         1 3967,7997285714287             3971,7997285714287 3967,0704285714282             4 1893329682
2025-11-05 08:53:20 XAUUSDm FARMER               1 3967,7997285714287             3969,7997285714287 3949,7997285714287             2 1893329692
2025-11-05 08:50:18 XAUUSDm INTRADAY_LOW         1  3970,858810714286              3974,858810714286  3970,274785714286             4 1893315194
2025-11-05 08:50:18 XAUUSDm FARMER               1  3970,858810714286              3972,858810714286  3952,858810714286             2 1893315205
2025-11-05 08:43:00 XAUUSDm SWING_HIGH           1 3972,7905357142854             3976,7905357142854 3971,4565714285714             4 1893285964
2025-11-05 08:42:30 XAUUSDm SWING_HIGH           1 3972,5398607142856             3976,5398607142856  3971,233571428571             4 1893283931
2025-11-05 08:41:59 XAUUSDm SWING_HIGH           1  3972,928867857143              3976,928867857143  3971,663285714286             4 1893281028
2025-11-05 08:41:28 XAUUSDm SWING_HIGH           1 3972,1387357142858             3976,1387357142858 3970,7965714285715             4 1893277886
2025-11-05 08:40:56 XAUUSDm SWING_HIGH           1  3971,807089285714              3975,807089285714 3970,4504285714283             4 1893274353
2025-11-05 08:40:25 XAUUSDm SWING_HIGH           1 3970,2348142857145             3974,2348142857145 3968,9714285714285             4 1893271854
2025-11-05 08:39:55 XAUUSDm SWING_HIGH           1 3969,8658857142855             3973,8658857142855 3968,4765714285713             4 1893270177
2025-11-05 08:38:27 XAUUSDm FARMER               1         3971,42185                     3973,42185         3953,42185             2 1893265842
2025-11-05 08:38:15 XAUUSDm INTRADAY_MED         1  3970,483642857143              3977,483642857143 3969,5027142857143             7 1893263051
2025-11-05 08:38:15 XAUUSDm FARMER               1  3970,483642857143              3972,483642857143  3952,483642857143             2 1893263077
2025-11-05 08:37:44 XAUUSDm INTRADAY_MED         1 3970,8554357142857             3977,8554357142857 3969,9119285714282             7 1893261044
2025-11-05 08:37:44 XAUUSDm FARMER               1 3970,8554357142857             3972,8554357142857 3952,8554357142857             2 1893261059
2025-11-05 08:37:13 XAUUSDm INTRADAY_MED         1 3972,0014642857145             3979,0014642857145 3970,9950714285715             7 1893258748
2025-11-05 08:37:13 XAUUSDm FARMER               1 3972,0014642857145             3974,0014642857145 3954,0014642857145             2 1893258756
2025-11-05 08:36:43 XAUUSDm INTRADAY_MED         1 3972,4873214285717             3979,4873214285717 3971,5163571428575             7 1893256519
2025-11-05 08:36:43 XAUUSDm FARMER               1 3972,4873214285717             3974,4873214285717 3954,4873214285717             2 1893256534
2025-11-05 08:36:10 XAUUSDm INTRADAY_MED         1  3972,174728571428              3979,174728571428 3971,2221428571424             7 1893253857
2025-11-05 08:36:10 XAUUSDm FARMER               1  3972,174728571428              3974,174728571428  3954,174728571428             2 1893253894
2025-11-05 08:35:38 XAUUSDm INTRADAY_MED         1 3971,5837464285714             3978,5837464285714  3970,661607142857             7 1893250667
2025-11-05 08:35:38 XAUUSDm FARMER               1 3971,5837464285714             3973,5837464285714 3953,5837464285714             2 1893250705
2025-11-05 08:35:07 XAUUSDm SWING_HIGH           1  3971,524432142857              3975,524432142857  3970,235714285714             4 1893248930
2025-11-05 08:34:06 XAUUSDm SWING_HIGH           1 3970,0937035714283             3974,0937035714283  3968,957857142857             4 1893242798
2025-11-05 08:33:34 XAUUSDm SWING_HIGH           1  3969,662428571429              3973,662428571429 3968,5378571428573             4 1893240309
2025-11-05 08:28:27 XAUUSDm SWING_HIGH           1  3968,142057142857              3972,142057142857  3966,622714285714             4 1893216653
2025-11-05 08:27:56 XAUUSDm SWING_HIGH           1 3968,6761428571426             3972,6761428571426 3967,1122857142855             4 1893214874
2025-11-05 08:27:27 XAUUSDm SWING_HIGH           1 3968,8524428571427             3972,8524428571427 3967,1122857142855             4 1893213373
2025-11-05 08:26:55 XAUUSDm SWING_HIGH           1 3969,0634785714287             3973,0634785714287 3967,3218571428574             4 1893211450
2025-11-05 08:26:24 XAUUSDm INTRADAY_MED        -1 3969,3314107142855             3962,3314107142855  3970,682678571429             7 1893209175
2025-11-05 08:26:24 XAUUSDm FARMER              -1 3969,3314107142855             3967,3314107142855 3987,3314107142855             2 1893209316
2025-11-05 08:25:53 XAUUSDm SWING_HIGH           1 3975,1323231554456             3979,1323231554456 3741,2140737821856             4 1893207338
2025-11-05 08:25:22 XAUUSDm SWING_HIGH           1   3974,55204623674               3978,55204623674 3736,0121505304064             4 1893205323
2025-11-05 08:24:51 XAUUSDm SWING_HIGH           1  3975,183983425558              3979,183983425558  3732,464662977682             4 1893201912
2025-11-05 08:24:20 XAUUSDm SWING_HIGH           1  3974,826911148865              3978,826911148865 3723,0085540454097             4 1893199403
2025-11-05 08:23:50 XAUUSDm SWING_HIGH           1  3973,535351982484              3977,535351982484  3716,122920700646             4 1893196890
2025-11-05 08:23:19 XAUUSDm SWING_HIGH           1  3972,898167965978              3976,898167965978 3710,5732813608856             4 1893194397
2025-11-05 08:22:48 XAUUSDm SWING_HIGH           1 3973,2141894109477             3977,2141894109477 3706,9114235620923             4 1893191978
2025-11-05 08:22:16 XAUUSDm SWING_HIGH           1 3973,1257132337078             3977,1257132337078 3701,1844706516913             4 1893189527
2025-11-05 08:21:45 XAUUSDm SWING_HIGH           1  3975,281380925958              3979,281380925958 3698,3107629616893             4 1893186063
2025-11-05 08:21:11 XAUUSDm SWING_HIGH           1 3972,7976310340878             3976,7976310340878  3691,511758636488             4 1893183384
2025-11-05 08:20:38 XAUUSDm SWING_HIGH           1   3972,05695915713               3976,05695915713  3686,821633714788             4 1893180115
2025-11-05 08:19:39 XAUUSDm SWING_HIGH           1 3973,5407549878855             3977,5407549878855  3683,885800484591             4 1893175805
2025-11-04 22:05:51 XAUUSDm SWING_HIGH          -1 3932,7320785714287             3928,7320785714287  3934,491857142857             4 1891448577
2025-11-04 22:05:45 XAUUSDm SWING_HIGH          -1         3933,09965                     3929,09965           3934,877             4 1891445320
2025-11-04 22:05:09 XAUUSDm SWING_HIGH          -1 3931,5321464285717             3927,5321464285717  3933,084142857143             4 1891441873
2025-11-04 22:04:08 XAUUSDm SWING_HIGH          -1 3933,4915499999997             3929,4915499999997           3934,822             4 1891435823
2025-11-04 22:02:44 XAUUSDm SWING_HIGH          -1  3936,686717857143              3932,686717857143  3937,641285714286             4 1891428331
2025-11-04 22:00:25 XAUUSDm SWING_HIGH          -1 3937,4014357142855             3933,4014357142855  3938,285571428571             4 1891418522
2025-11-04 21:54:06 XAUUSDm SWING_HIGH          -1  3937,521185714286              3933,521185714286 3938,4155714285716             4 1891388750
2025-11-04 21:53:26 XAUUSDm SWING_HIGH          -1  3937,760557142857              3933,760557142857 3938,6397142857145             4 1891386737
2025-11-04 21:51:39 XAUUSDm SWING_HIGH          -1 3937,4536464285716             3933,4536464285716  3938,534142857143             4 1891380968
2025-11-04 21:50:59 XAUUSDm SWING_HIGH          -1  3936,942192857143              3932,942192857143 3938,0412857142856             4 1891378273
2025-11-04 21:50:30 XAUUSDm SWING_HIGH          -1  3937,059389285714              3933,059389285714 3938,1914285714283             4 1891375596
2025-11-04 21:49:54 XAUUSDm SWING_HIGH          -1 3936,6014785714287             3932,6014785714287  3937,688857142857             4 1891372137
2025-11-04 21:49:12 XAUUSDm SWING_HIGH          -1  3937,684432142857              3933,684432142857  3938,691714285714             4 1891368465
2025-11-04 21:46:46 XAUUSDm SWING_HIGH          -1  3937,425410714286              3933,425410714286  3938,597571428572             4 1891358167
2025-11-04 21:46:15 XAUUSDm SWING_HIGH          -1 3936,7753285714284             3932,7753285714284  3937,991857142857             4 1891355940
2025-11-04 21:45:45 XAUUSDm SWING_HIGH          -1        3937,097625                    3933,097625           3938,302             4 1891353167
2025-11-04 21:45:15 XAUUSDm SWING_HIGH          -1 3937,5047285714286             3933,5047285714286 3938,7048571428572             4 1891350856
2025-11-04 21:44:44 XAUUSDm SWING_HIGH          -1  3938,163610714286              3934,163610714286 3939,3685714285716             4 1891347782
2025-11-04 21:41:46 XAUUSDm SWING_HIGH          -1 3940,0011607142856             3936,0011607142856 3941,0605714285716             4 1891328240
2025-11-04 21:41:18 XAUUSDm SWING_HIGH          -1 3940,8140035714287             3936,8140035714287 3941,7568571428574             4 1891325081
2025-11-04 21:40:04 XAUUSDm SWING_HIGH          -1 3941,1086892857143             3937,1086892857143  3942,064428571429             4 1891321134
2025-11-04 21:39:34 XAUUSDm SWING_HIGH          -1 3941,2612714285715             3937,2612714285715  3942,275142857143             4 1891318789
2025-11-04 21:28:56 XAUUSDm SWING_HIGH           1 3942,5566821428574             3946,5566821428574 3941,5447142857142             4 1891263157
2025-11-04 21:28:25 XAUUSDm SWING_HIGH           1  3942,718332142857              3946,718332142857  3941,597714285714             4 1891261274
2025-11-04 21:27:16 XAUUSDm SWING_HIGH           1 3942,5635964285716             3946,5635964285716  3941,268142857143             4 1891256443
2025-11-04 21:25:45 XAUUSDm SWING_HIGH           1  3943,302514285714              3947,302514285714 3942,1334285714283             4 1891250644
2025-11-04 21:25:17 XAUUSDm SWING_HIGH           1 3942,9909428571427             3946,9909428571427  3941,804285714286             4 1891246412
2025-11-04 21:20:57 XAUUSDm SWING_HIGH           1  3941,667114285714              3945,667114285714 3939,5304285714283             4 1891226513
2025-11-04 20:37:37 XAUUSDm SWING_HIGH           1 3941,5224565904546             3945,5224565904546 3756,4297363818127             4 1891002204
2025-11-04 20:37:01 XAUUSDm SWING_HIGH           1  3940,436751689702              3944,436751689702  3749,263932411915             4 1890998940
2025-11-04 20:36:26 XAUUSDm SWING_HIGH           1 3943,9781300989653             3947,9781300989653 3748,1157960413907             4 1890993852
2025-11-04 20:35:54 XAUUSDm SWING_HIGH           1 3946,4808826666776             3950,4808826666776  3746,528693332885             4 1890985152
2025-11-04 20:35:05 XAUUSDm SWING_HIGH           1  3948,413715586736              3952,413715586736 3745,3113765305625             4 1890978710
2025-11-04 20:34:07 XAUUSDm SWING_HIGH           1 3947,7365948448287             3951,7365948448287  3738,735206206865             4 1890973263
2025-11-04 20:33:33 XAUUSDm SWING_HIGH           1 3949,0155614127957             3953,0155614127957  3738,170543488171             4 1890968479
2025-11-04 20:33:06 US30m   SWING_HIGH           1  47238,58333060237              47242,58333060237  40748,96677590536             4 1890964839
2025-11-04 20:33:05 XAUUSDm SWING_HIGH           1  3948,477533672135              3952,477533672135  3732,098653114585             4 1890964652
2025-11-04 20:32:34 US30m   SWING_HIGH           1   47246,4858026607               47250,4858026607  40752,66789357193             4 1890960571
2025-11-04 20:32:32 XAUUSDm SWING_HIGH           1 3951,2625427322846             3955,2625427322846 3728,4872907086146             4 1890960340
2025-11-04 17:00:56 XAUUSDm SWING_HIGH           1 3956,4259357142855             3960,4259357142855 3953,2305714285712             4 1889671889
2025-11-04 17:00:26 XAUUSDm SWING_HIGH           1  3958,035232142857              3962,035232142857  3954,909714285714             4 1889668692
2025-11-04 16:59:55 XAUUSDm SWING_HIGH           1 3957,8245464285715             3961,8245464285715 3954,6451428571427             4 1889664820
2025-11-04 16:59:24 XAUUSDm SWING_HIGH           1 3957,6437571428573             3961,6437571428573  3954,414714285714             4 1889660152
2025-11-04 16:58:54 XAUUSDm SWING_HIGH           1 3956,3722857142857             3960,3722857142857 3953,2445714285714             4 1889656003
2025-11-04 16:58:23 XAUUSDm SWING_HIGH           1 3954,4744357142854             3958,4744357142854 3951,4635714285714             4 1889652044
2025-11-04 16:57:22 XAUUSDm SWING_HIGH           1  3951,576407142857              3955,576407142857 3948,8127142857143             4 1889646290
2025-11-04 16:56:50 XAUUSDm SWING_HIGH           1 3953,1330035714286             3957,1330035714286  3950,508857142857             4 1889642712
2025-11-04 16:56:20 XAUUSDm SWING_HIGH           1         3953,74185                     3957,74185            3950,96             4 1889639408
2025-11-04 16:55:48 XAUUSDm SWING_HIGH           1         3953,52515                     3957,52515           3950,567             4 1889635497
2025-11-04 16:55:16 XAUUSDm SWING_HIGH           1 3951,0846464285714             3955,0846464285714  3948,352142857143             4 1889631057
2025-11-04 16:45:38 XAUUSDm SWING_HIGH          -1 3935,0967178571427             3931,0967178571427 3939,3722857142857             4 1889556982
2025-11-04 16:45:06 XAUUSDm SWING_HIGH          -1 3933,8140785714286             3929,8140785714286 3937,9928571428572             4 1889552130
2025-11-04 16:44:36 XAUUSDm SWING_HIGH          -1  3933,454796428571              3929,454796428571  3938,137142857143             4 1889546168
2025-11-04 16:43:35 XAUUSDm SWING_HIGH          -1  3934,337728571428              3930,337728571428  3938,940857142857             4 1889536016
2025-11-04 16:42:34 XAUUSDm SWING_HIGH          -1 3933,0889392857143             3929,0889392857143 3936,5764285714286             4 1889524217
2025-11-04 16:38:10 XAUUSDm SWING_HIGH          -1 3938,1899785714286             3934,1899785714286 3941,9628571428575             4 1889470626
2025-11-04 16:37:41 XAUUSDm SWING_HIGH          -1 3937,5551499999997             3933,5551499999997           3941,772             4 1889463799
2025-11-04 16:37:09 XAUUSDm SWING_HIGH          -1 3941,3456464285714             3937,3456464285714  3945,378142857143             4 1889458595
2025-11-04 16:36:32 XAUUSDm SWING_HIGH          -1 3938,8365035714287             3934,8365035714287 3944,5558571428573             4 1889451601
2025-11-04 16:36:01 XAUUSDm SWING_HIGH          -1  3936,332342857143              3932,332342857143 3941,7302857142854             4 1889443652
2025-11-04 16:35:30 XAUUSDm SWING_HIGH          -1  3936,224867857143              3932,224867857143 3941,7652857142857             4 1889439138
2025-11-04 16:35:00 XAUUSDm SWING_HIGH          -1  3937,147932142857              3933,147932142857 3942,6037142857144             4 1889431582
2025-11-04 16:34:30 XAUUSDm SWING_HIGH          -1 3937,4931714285717             3933,4931714285717  3942,939142857143             4 1889423122
2025-11-04 16:33:58 XAUUSDm SWING_HIGH          -1 3941,3779000000004             3937,3779000000004           3946,425             4 1889414063
2025-11-04 16:33:28 XAUUSDm SWING_HIGH          -1 3943,4507928571425             3939,4507928571425 3948,5432857142855             4 1889406716
2025-11-04 16:32:56 XAUUSDm SWING_HIGH          -1        3945,707975                    3941,707975           3950,547             4 1889397642
2025-11-04 16:32:21 XAUUSDm SWING_HIGH          -1          3949,0585                      3945,0585 3953,5480000000002             4 1889388727
2025-11-04 16:31:48 XAUUSDm SWING_HIGH          -1 3951,5307285714284             3947,5307285714284  3955,723857142857             4 1889378314
2025-11-04 16:31:05 XAUUSDm SWING_HIGH          -1  3952,000785714286              3948,000785714286 3956,3145714285715             4 1889369386
2025-11-04 16:30:37 XAUUSDm SWING_HIGH          -1  3952,525207142857              3948,525207142857  3956,903714285714             4 1889363346
2025-11-04 16:30:06 XAUUSDm SWING_HIGH          -1 3956,1925892857143             3952,1925892857143  3960,104428571429             4 1889356931
2025-11-04 16:28:20 XAUUSDm SWING_HIGH          -1        3967,387875                    3963,387875 3969,1969999999997             4 1889323261
2025-11-04 16:27:27 XAUUSDm SWING_HIGH          -1 3968,4609107142855             3964,4609107142855 3970,4325714285715             4 1889319415
2025-11-04 16:27:03 XAUUSDm SWING_HIGH          -1          3968,8039                      3964,8039           3970,776             4 1889314801
2025-11-04 16:26:31 XAUUSDm SWING_HIGH          -1  3969,079110714286              3965,079110714286 3971,1655714285716             4 1889312560
2025-11-04 16:25:47 XAUUSDm SWING_HIGH          -1 3970,2307142857144             3966,2307142857144 3972,2924285714284             4 1889309604
2025-11-04 16:10:07 XAUUSDm SWING_HIGH          -1         3970,13085                     3966,13085           3971,408             4 1889202165
2025-11-04 16:06:58 XAUUSDm SWING_HIGH          -1 3970,8458250000003             3966,8458250000003 3972,9030000000002             4 1889181786
2025-11-04 16:06:22 XAUUSDm SWING_HIGH          -1 3969,7336642857144             3965,7336642857144 3971,6744285714285             4 1889176179
2025-11-04 16:05:29 XAUUSDm SWING_HIGH          -1  3968,498928571428              3964,498928571428  3970,346857142857             4 1889162366
2025-11-04 16:04:42 XAUUSDm SWING_HIGH          -1 3969,7393142857145             3965,7393142857145 3971,4074285714287             4 1889156018
2025-11-04 16:04:10 XAUUSDm SWING_HIGH          -1  3969,060692857143              3965,060692857143  3970,795285714286             4 1889151264
2025-11-04 16:02:52 XAUUSDm SWING_HIGH          -1         3970,30155                     3966,30155           3971,878             4 1889140763
2025-11-04 16:02:34 XAUUSDm SWING_HIGH          -1 3970,1736928571427             3966,1736928571427 3971,9902857142856             4 1889135606
2025-11-04 16:01:55 XAUUSDm SWING_HIGH          -1 3970,1992214285715             3966,1992214285715 3972,5271428571427             4 1889131167
2025-11-04 16:01:06 XAUUSDm SWING_HIGH          -1 3971,2925642857144             3967,2925642857144 3973,4834285714282             4 1889125357
2025-11-04 16:00:00 XAUUSDm SWING_HIGH          -1  3975,396453571429              3971,396453571429  3977,304857142857             4 1889109353
2025-11-04 15:59:35 XAUUSDm SWING_HIGH          -1 3976,0422249999997             3972,0422249999997           3978,124             4 1889104705
2025-11-04 15:59:04 XAUUSDm SWING_HIGH          -1  3977,242157142857              3973,242157142857  3979,285714285714             4 1889101921
2025-11-04 15:57:30 XAUUSDm SWING_HIGH          -1         3976,24225                     3972,24225           3978,446             4 1889092589
2025-11-04 15:54:18 XAUUSDm SWING_HIGH          -1  3975,102492857143              3971,102492857143  3977,337285714286             4 1889071366
2025-11-04 15:53:14 XAUUSDm SWING_HIGH          -1  3975,307221428571              3971,307221428571  3977,512142857143             4 1889064956
2025-11-04 15:50:44 XAUUSDm SWING_HIGH          -1  3976,494435714286              3972,494435714286 3978,2805714285714             4 1889045294
2025-11-04 15:50:03 XAUUSDm SWING_HIGH          -1  3976,648057142857              3972,648057142857 3978,4497142857144             4 1889031883
2025-11-04 15:48:09 XAUUSDm SWING_HIGH          -1  3978,811407142857              3974,811407142857 3980,8037142857142             4 1889016266
2025-11-04 15:45:33 XAUUSDm SWING_HIGH          -1 3980,0588357142856             3976,0588357142856 3982,7305714285712             4 1888994226
2025-11-04 15:40:48 XAUUSDm SWING_HIGH          -1 3981,1893250000003             3977,1893250000003           3985,153             4 1888957059
2025-11-04 15:39:41 XAUUSDm SWING_HIGH          -1          3978,3784                      3974,3784           3981,929             4 1888949618
2025-11-04 15:38:09 XAUUSDm SWING_HIGH          -1  3979,286692857143              3975,286692857143 3982,1692857142857             4 1888925684
2025-11-04 15:37:11 XAUUSDm SWING_HIGH          -1 3982,0555464285712             3978,0555464285712  3984,534142857143             4 1888919536
2025-11-04 15:35:49 XAUUSDm SWING_HIGH          -1  3980,232082142857              3976,232082142857 3982,4427142857144             4 1888907869
2025-11-04 15:35:08 XAUUSDm SWING_HIGH          -1  3979,046332142857              3975,046332142857 3981,0827142857142             4 1888897528
2025-11-04 15:33:33 XAUUSDm SWING_HIGH          -1 3985,3792857142857             3981,3792857142857 3986,5155714285715             4 1888875270
2025-11-04 15:32:05 XAUUSDm SWING_HIGH          -1 3986,8884749999997             3982,8884749999997           3987,976             4 1888870521
2025-11-04 15:25:47 XAUUSDm SWING_HIGH          -1  3987,159214285714              3983,159214285714 3987,6424285714284             4 1888852593
2025-11-04 15:19:40 XAUUSDm SWING_HIGH           1 3993,2705178571427             3997,2705178571427  3992,060285714286             4 1888747569
2025-11-04 15:17:00 XAUUSDm SWING_HIGH           1 3994,4519214285715             3998,4519214285715 3993,0201428571427             4 1888726788
2025-11-04 15:16:02 XAUUSDm SWING_HIGH           1  3992,812246428571              3996,812246428571 3991,4081428571426             4 1888719903
2025-11-04 15:15:18 XAUUSDm SWING_HIGH           1  3993,593835714286              3997,593835714286 3992,2065714285714             4 1888713785
2025-11-04 15:13:00 XAUUSDm SWING_HIGH           1 3994,6258714285714             3998,6258714285714  3993,155142857143             4 1888697164
2025-11-04 15:12:29 XAUUSDm SWING_HIGH           1  3993,565417857143              3997,565417857143  3992,113285714286             4 1888692953
2025-11-04 15:11:02 XAUUSDm SWING_HIGH           1  3992,678632142857              3996,678632142857 3991,3407142857145             4 1888681099
2025-11-04 15:00:54 XAUUSDm SWING_HIGH          -1           3985,575                       3981,575 3986,8869999999997             4 1888605152
2025-11-04 15:00:03 XAUUSDm SWING_HIGH          -1  3984,925607142857              3980,925607142857 3986,2537142857145             4 1888599494
2025-11-04 14:59:44 XAUUSDm SWING_HIGH          -1 3984,9473857142857             3980,9473857142857  3986,366571428571             4 1888595384
2025-11-04 14:59:00 XAUUSDm SWING_HIGH          -1  3985,331442857143              3981,331442857143  3986,953285714286             4 1888590866
2025-11-04 14:58:21 XAUUSDm SWING_HIGH          -1 3985,7117642857143             3981,7117642857143 3987,2794285714285             4 1888587743
2025-11-04 14:57:33 XAUUSDm SWING_HIGH          -1 3986,4222357142858             3982,4222357142858  3987,888571428571             4 1888584137
2025-11-04 14:56:41 XAUUSDm SWING_HIGH          -1          3985,0394                      3981,0394           3986,458             4 1888577258
2025-11-04 14:55:57 XAUUSDm SWING_HIGH          -1 3984,8095321428573             3980,8095321428573  3986,304714285714             4 1888572063
2025-11-04 14:55:17 XAUUSDm SWING_HIGH          -1 3984,5171464285713             3980,5171464285713 3985,9871428571423             4 1888566357
2025-11-04 14:54:34 XAUUSDm SWING_HIGH          -1 3985,9296178571426             3981,9296178571426 3987,3392857142853             4 1888560963
2025-11-04 14:52:40 XAUUSDm SWING_HIGH          -1  3988,173792857143              3984,173792857143 3989,5352857142852             4 1888545170
2025-11-04 14:52:02 XAUUSDm SWING_HIGH          -1 3987,4140607142854             3983,4140607142854  3988,805571428571             4 1888541942
2025-11-04 14:50:01 XAUUSDm SWING_HIGH          -1         3988,54655                     3984,54655 3989,7129999999997             4 1888529093
2025-11-04 14:49:34 XAUUSDm SWING_HIGH          -1         3988,55555                     3984,55555 3989,7219999999998             4 1888525350
2025-11-04 14:21:38 XAUUSDm SWING_HIGH           1 3996,1559785714285             4000,1559785714285 3995,3368571428573             4 1888311936
2025-11-04 14:17:28 XAUUSDm SWING_HIGH           1 3996,6064714285717             4000,6064714285717 3995,9311428571427             4 1888302630
2025-11-04 14:13:32 XAUUSDm SWING_HIGH          -1 3994,7008857142855             3990,7008857142855 3995,4025714285713             4 1888269630
2025-11-04 14:12:50 XAUUSDm SWING_HIGH          -1        3995,021425                    3991,021425           3995,701             4 1888265902
2025-11-04 14:11:51 XAUUSDm SWING_HIGH          -1 3994,7781714285716             3990,7781714285716 3995,6321428571428             4 1888259425
2025-11-04 14:11:02 XAUUSDm SWING_HIGH          -1 3994,3339928571427             3990,3339928571427 3995,1542857142854             4 1888255747
2025-11-04 14:10:35 XAUUSDm SWING_HIGH          -1 3994,7428214285715             3990,7428214285715  3995,570142857143             4 1888251969
2025-11-04 14:09:22 XAUUSDm SWING_HIGH           1 3995,3057785714286             3999,3057785714286 3994,2898571428573             4 1888247312
2025-11-04 14:08:53 XAUUSDm SWING_HIGH           1 3995,6787785714287             3999,6787785714287 3994,7038571428575             4 1888245391
2025-11-04 14:08:21 XAUUSDm SWING_HIGH           1 3995,5406428571428             3999,5406428571428  3994,530285714286             4 1888243340
2025-11-04 14:07:38 XAUUSDm SWING_HIGH           1 3995,9989035714284             3999,9989035714284  3994,936857142857             4 1888240148
2025-11-04 14:05:41 XAUUSDm SWING_HIGH           1 3995,4915928571427             3999,4915928571427  3994,442285714286             4 1888231000
2025-11-04 14:04:10 XAUUSDm SWING_HIGH           1 3995,5660535714283             3999,5660535714283  3994,374857142857             4 1888223302
2025-11-04 14:03:41 XAUUSDm SWING_HIGH           1 3995,7816357142856             3999,7816357142856 3994,5665714285715             4 1888220953
2025-11-04 13:54:41 XAUUSDm SWING_HIGH           1        3995,540525                    3999,540525           3993,756             4 1888169096
2025-11-04 13:53:39 XAUUSDm SWING_HIGH           1  3997,071553571429              4001,071553571429 3995,3678571428577             4 1888163014
2025-11-04 13:52:46 XAUUSDm SWING_HIGH           1 3997,3973464285714             4001,3973464285714  3995,661142857143             4 1888159338
2025-11-04 13:51:32 XAUUSDm SWING_HIGH           1  3998,298864285714              4002,298864285714 3996,6234285714286             4 1888151705
2025-11-04 13:50:54 XAUUSDm SWING_HIGH           1  3999,307128571428              4003,307128571428  3997,743857142857             4 1888147160
2025-11-04 11:50:04 XAUUSDm SWING_HIGH           1 4000,1801885552663             4004,1801885552663 3741,5854577893424             4 1887520734
2025-11-04 11:50:04 US30m   SWING_HIGH           1  47139,50218015249              47143,50218015249  40587,61279390009             4 1887520764
2025-11-04 11:49:33 XAUUSDm SWING_HIGH           1 4001,6392749766724             4005,6392749766724 3736,1120009331103             4 1887517545
2025-11-04 11:49:33 US30m   SWING_HIGH           1 47152,179996565756             47156,179996565756  40597,10013736994             4 1887517592
2025-11-04 11:49:03 XAUUSDm SWING_HIGH           1   4001,46461200058               4005,46461200058 3727,7645199768017             4 1887514023
2025-11-04 11:49:02 US30m   SWING_HIGH           1  47149,78324817868              47153,78324817868  40590,47007285279             4 1887514120
2025-11-04 11:48:32 XAUUSDm SWING_HIGH           1  4000,646785066806              4004,646785066806 3723,9465973277674             4 1887511314
2025-11-04 11:48:32 US30m   SWING_HIGH           1  47142,21380502946              47146,21380502946  40581,64779882136             4 1887511363





PS C:\Users\ndlal\getrichfrbot> $resp = Invoke-RestMethod "http://localhost:5000/api/recent_trades?hours=24&limit=2000"
PS C:\Users\ndlal\getrichfrbot> $sw = $resp.trades | Where-Object { $_.engine -eq 'SWING_HIGH' -and $_.status -eq 'CLOSED' }
PS C:\Users\ndlal\getrichfrbot>
PS C:\Users\ndlal\getrichfrbot> # Helper to parse numbers even if commas are decimal separators
PS C:\Users\ndlal\getrichfrbot> function ParseD($v) { [double]::Parse(("$v").Replace(',', '.'), [System.Globalization.CultureInfo]::InvariantCulture) }
PS C:\Users\ndlal\getrichfrbot>
PS C:\Users\ndlal\getrichfrbot> $enriched = $sw | ForEach-Object {
>>   $entry = ParseD $_.entry
>>   $dir   = [int]$_.direction
>>
>>   $closeEff = $null
>>   if ($_.close_price) { $closeEff = ParseD $_.close_price }
>>   elseif ($_.tp)     { $closeEff = ParseD $_.tp }
>>   elseif ($_.sl)     { $closeEff = ParseD $_.sl }
>>
>>   if ($null -ne $closeEff) {
>>     $pp = if ($dir -eq 1) { $closeEff - $entry } else { $entry - $closeEff }
>>     $_ | Add-Member -NotePropertyName profit_points -NotePropertyValue $pp -PassThru
>>   }
>> }
PS C:\Users\ndlal\getrichfrbot>
PS C:\Users\ndlal\getrichfrbot> $winners = $enriched | Where-Object { $_.profit_points -gt 0 }
PS C:\Users\ndlal\getrichfrbot>
PS C:\Users\ndlal\getrichfrbot> $winners |
>>   Select-Object timestamp, symbol, engine, direction, entry, close_price, tp, sl, profit_points, ticket |
>>   Format-Table -AutoSize

timestamp           symbol  engine     direction              entry close_price                 tp                 sl profit_points     ticket
---------           ------  ------     ---------              ----- -----------                 --                 -- -------------     ------
2025-11-05 12:09:26 XAUUSDm SWING_HIGH        -1 3963,0138464285715             3959,0138464285715  3965,644142857143             4 1894418179
2025-11-05 12:08:22 XAUUSDm SWING_HIGH        -1 3963,0166214285714             3959,0166214285714  3965,820142857143             4 1894411682
2025-11-05 12:07:32 XAUUSDm SWING_HIGH        -1 3958,3772357142857             3954,3772357142857 3960,4995714285715             4 1894405701
2025-11-05 12:07:05 XAUUSDm SWING_HIGH        -1        3958,929475                    3954,929475           3961,083             4 1894399907
2025-11-05 12:06:34 XAUUSDm SWING_HIGH        -1  3962,154732142857              3958,154732142857 3963,8467142857144             4 1894388941
2025-11-05 12:06:04 XAUUSDm SWING_HIGH        -1 3962,6315999999997             3958,6315999999997 3964,3289999999997             4 1894385692
2025-11-05 12:05:20 XAUUSDm SWING_HIGH        -1 3962,6043642857144             3958,6043642857144  3964,352428571429             4 1894381085
2025-11-05 12:04:49 XAUUSDm SWING_HIGH        -1 3962,7174714285716             3958,7174714285716 3964,4611428571434             4 1894376130
2025-11-05 12:04:18 XAUUSDm SWING_HIGH        -1  3962,993989285714              3958,993989285714  3964,716428571429             4 1894372262
2025-11-05 12:03:48 XAUUSDm SWING_HIGH        -1  3962,175832142857              3958,175832142857 3963,8227142857145             4 1894367485
2025-11-05 11:59:44 XAUUSDm SWING_HIGH         1  3971,702857142857              3975,702857142857  3971,134714285714             4 1894333116
2025-11-05 11:59:12 XAUUSDm SWING_HIGH         1        3971,642575                    3975,642575           3971,004             4 1894331627
2025-11-05 11:58:42 XAUUSDm SWING_HIGH         1 3971,1273607142857             3975,1273607142857 3970,5385714285712             4 1894329689
2025-11-05 11:57:41 XAUUSDm SWING_HIGH        -1 3970,6419428571426             3966,6419428571426 3971,3002857142856             4 1894326394
2025-11-05 11:51:04 XAUUSDm SWING_HIGH        -1  3970,074507142857              3966,074507142857  3971,037714285714             4 1894295112
2025-11-05 11:49:33 XAUUSDm SWING_HIGH        -1 3970,3144964285716             3966,3144964285716  3971,278142857143             4 1894288949
2025-11-05 11:47:01 XAUUSDm SWING_HIGH        -1 3969,1045107142854             3965,1045107142854  3969,903571428571             4 1894275593
2025-11-05 11:40:22 XAUUSDm SWING_HIGH        -1  3970,251021428571              3966,251021428571 3972,3821428571428             4 1894245071
2025-11-05 11:39:51 XAUUSDm SWING_HIGH        -1 3969,6093214285715             3965,6093214285715  3971,646142857143             4 1894241689
2025-11-05 11:39:20 XAUUSDm SWING_HIGH        -1 3967,8625821428573             3963,8625821428573  3969,642714285714             4 1894238494
2025-11-05 11:38:50 XAUUSDm SWING_HIGH        -1 3968,0893892857143             3964,0893892857143 3969,8364285714288             4 1894236302
2025-11-05 11:38:19 XAUUSDm SWING_HIGH        -1 3967,6788607142853             3963,6788607142853 3969,3655714285715             4 1894234413
2025-11-05 11:37:50 XAUUSDm SWING_HIGH        -1 3967,7350607142857             3963,7350607142857 3969,4135714285712             4 1894231964
2025-11-05 11:37:15 XAUUSDm SWING_HIGH        -1 3968,0448071428573             3964,0448071428573 3969,6927142857144             4 1894228797
2025-11-05 11:36:44 XAUUSDm SWING_HIGH        -1 3969,0379107142858             3965,0379107142858 3970,6405714285715             4 1894225289
2025-11-05 11:36:14 XAUUSDm SWING_HIGH        -1  3969,049039285714              3965,049039285714 3970,6874285714284             4 1894223112
2025-11-05 11:35:31 XAUUSDm SWING_HIGH        -1  3969,109346428572              3965,109346428572  3970,981142857143             4 1894220914
2025-11-05 11:16:37 XAUUSDm SWING_HIGH        -1         3972,90385                     3968,90385           3974,222             4 1894102564
2025-11-05 11:11:06 XAUUSDm SWING_HIGH        -1  3977,290503571429              3973,290503571429  3978,130857142857             4 1894063514
2025-11-05 11:02:13 XAUUSDm SWING_HIGH        -1        3978,319075                    3974,319075           3979,505             4 1893990149
2025-11-05 11:01:42 XAUUSDm SWING_HIGH        -1 3978,5380571428573             3974,5380571428573 3979,7657142857142             4 1893987892
2025-11-05 11:01:13 XAUUSDm SWING_HIGH        -1  3978,101532142857              3974,101532142857  3979,309714285714             4 1893985901
2025-11-05 11:00:42 XAUUSDm SWING_HIGH        -1  3977,992357142857              3973,992357142857 3979,2077142857142             4 1893983139
2025-11-05 10:59:41 XAUUSDm SWING_HIGH        -1 3980,0518178571433             3976,0518178571433 3981,0842857142857             4 1893974499
2025-11-05 10:51:57 XAUUSDm SWING_HIGH        -1  3980,884128571429              3976,884128571429  3981,739857142857             4 1893934332
2025-11-05 10:50:43 XAUUSDm SWING_HIGH        -1  3980,279582142857              3976,279582142857 3981,1987142857142             4 1893928704
2025-11-05 10:42:45 XAUUSDm SWING_HIGH         1 3984,2207285714285             3988,2207285714285 3983,3298571428572             4 1893891943
2025-11-05 10:42:15 XAUUSDm SWING_HIGH         1 3984,4633357142857             3988,4633357142857 3983,5065714285715             4 1893889872
2025-11-05 10:41:44 XAUUSDm SWING_HIGH         1 3984,4918071428574             3988,4918071428574 3983,4747142857145             4 1893887980
2025-11-05 10:41:14 XAUUSDm SWING_HIGH         1 3984,4165892857145             3988,4165892857145 3983,3674285714287             4 1893885526
2025-11-05 10:39:53 XAUUSDm SWING_HIGH         1 3984,7924392857144             3988,7924392857144 3983,6264285714287             4 1893878491
2025-11-05 10:39:23 XAUUSDm SWING_HIGH         1 3984,8603035714286             3988,8603035714286 3983,6588571428574             4 1893876080
2025-11-05 10:38:53 XAUUSDm SWING_HIGH         1  3984,958207142857              3988,958207142857  3983,555714285714             4 1893872631
2025-11-05 10:38:22 XAUUSDm SWING_HIGH         1 3984,8227464285715             3988,8227464285715  3983,398142857143             4 1893869719
2025-11-05 10:30:48 XAUUSDm SWING_HIGH        -1  3980,139842857143              3976,139842857143 3981,5402857142853             4 1893828159
2025-11-05 10:30:18 XAUUSDm SWING_HIGH        -1  3980,548760714286              3976,548760714286 3982,0345714285713             4 1893825577
2025-11-05 10:29:47 XAUUSDm SWING_HIGH        -1 3979,5524571428573             3975,5524571428573 3981,0097142857144             4 1893821286
2025-11-05 10:29:17 XAUUSDm SWING_HIGH        -1 3978,9951535714285             3974,9951535714285 3980,3828571428567             4 1893818402
2025-11-05 10:28:47 XAUUSDm SWING_HIGH        -1 3980,0591857142854             3976,0591857142854  3981,445571428571             4 1893815386
2025-11-05 10:28:16 XAUUSDm SWING_HIGH        -1  3979,305017857143              3975,305017857143 3980,7392857142854             4 1893811630
2025-11-05 10:19:05 XAUUSDm SWING_HIGH         1 3983,9891714285714             3987,9891714285714  3982,342142857143             4 1893756437
2025-11-05 10:11:33 XAUUSDm SWING_HIGH         1 3982,8184107142856             3986,8184107142856 3979,7265714285713             4 1893710154
2025-11-05 10:10:00 XAUUSDm SWING_HIGH         1  3986,436603571429              3990,436603571429 3983,6648571428573             4 1893700050
2025-11-05 10:09:31 XAUUSDm SWING_HIGH         1 3985,5940571428573             3989,5940571428573 3982,9267142857143             4 1893695507
2025-11-05 10:08:54 XAUUSDm SWING_HIGH         1        3986,150425                    3990,150425            3983,55             4 1893692255
2025-11-05 10:07:51 XAUUSDm SWING_HIGH         1 3984,0667714285714             3988,0667714285714  3981,616142857143             4 1893683036
2025-11-05 10:07:19 XAUUSDm SWING_HIGH         1 3985,4036107142856             3989,4036107142856 3983,1235714285713             4 1893678665
2025-11-05 10:06:47 XAUUSDm SWING_HIGH         1  3984,514682142857              3988,514682142857  3982,354714285714             4 1893673876
2025-11-05 10:06:17 XAUUSDm SWING_HIGH         1 3982,2249642857146             3986,2249642857146 3980,3404285714287             4 1893668999
2025-11-05 10:05:09 XAUUSDm SWING_HIGH         1 3977,0433357142856             3981,0433357142856 3975,7175714285713             4 1893652676
2025-11-05 10:03:36 XAUUSDm SWING_HIGH         1  3973,623085714286              3977,623085714286 3972,4305714285715             4 1893640962
2025-11-05 10:03:06 XAUUSDm SWING_HIGH         1  3974,293985714286              3978,293985714286 3973,1465714285714             4 1893638295
2025-11-05 10:02:35 XAUUSDm SWING_HIGH         1  3975,060457142857              3979,060457142857 3973,9757142857143             4 1893635764
2025-11-05 10:02:06 XAUUSDm SWING_HIGH         1  3975,188160714286              3979,188160714286 3974,0745714285713             4 1893633648
2025-11-05 10:01:33 XAUUSDm SWING_HIGH         1 3975,0888178571427             3979,0888178571427 3973,9072857142855             4 1893630582
2025-11-05 09:58:59 XAUUSDm SWING_HIGH         1        3973,421375                    3977,421375           3972,422             4 1893614700
2025-11-05 09:58:29 XAUUSDm SWING_HIGH         1          3973,8235                      3977,8235           3972,819             4 1893612848
2025-11-05 09:57:58 XAUUSDm SWING_HIGH         1          3973,9328                      3977,9328           3972,875             4 1893610292
2025-11-05 09:57:26 XAUUSDm SWING_HIGH         1  3972,685785714286              3976,685785714286 3971,7515714285714             4 1893605886
2025-11-05 09:56:56 XAUUSDm SWING_HIGH         1 3972,0549892857143             3976,0549892857143 3971,1534285714283             4 1893602296
2025-11-05 09:55:54 XAUUSDm SWING_HIGH         1 3970,1754071428572             3974,1754071428572 3969,3797142857143             4 1893598340
2025-11-05 09:53:21 XAUUSDm SWING_HIGH         1  3970,285989285714              3974,285989285714 3969,5074285714286             4 1893590339
2025-11-05 09:51:49 XAUUSDm SWING_HIGH         1  3970,449489285714              3974,449489285714 3969,4044285714285             4 1893586618
2025-11-05 09:51:18 XAUUSDm SWING_HIGH         1 3970,8882642857143             3974,8882642857143 3969,7704285714285             4 1893585357
2025-11-05 09:50:44 XAUUSDm SWING_HIGH         1 3971,3655821428574             3975,3655821428574 3970,0297142857144             4 1893582654
2025-11-05 09:44:43 XAUUSDm SWING_HIGH         1           3970,378                       3974,378           3968,779             4 1893563062
2025-11-05 09:44:11 XAUUSDm SWING_HIGH         1  3970,577482142857              3974,577482142857  3968,958714285714             4 1893561531
2025-11-05 09:43:41 XAUUSDm SWING_HIGH         1 3969,5763785714284             3973,5763785714284  3967,879857142857             4 1893559750
2025-11-05 09:43:10 XAUUSDm SWING_HIGH         1 3970,5115464285714             3974,5115464285714  3968,767142857143             4 1893557170
2025-11-05 09:40:52 XAUUSDm SWING_HIGH         1 3968,9683785714287             3972,9683785714287  3967,435857142857             4 1893549765
2025-11-05 09:40:15 XAUUSDm SWING_HIGH         1  3969,592142857143              3973,592142857143  3968,151285714285             4 1893547188
2025-11-05 09:39:52 XAUUSDm SWING_HIGH         1          3970,1061                      3974,1061           3968,667             4 1893545058
2025-11-05 09:39:12 XAUUSDm SWING_HIGH         1 3969,3935214285716             3973,3935214285716  3968,019142857143             4 1893542598
2025-11-05 09:38:41 XAUUSDm SWING_HIGH         1  3968,487814285714              3972,487814285714 3967,1834285714285             4 1893540554
2025-11-05 09:38:12 XAUUSDm SWING_HIGH         1 3969,1219107142856             3973,1219107142856  3967,854571428571             4 1893538842
2025-11-05 09:37:42 XAUUSDm SWING_HIGH         1  3968,879303571429              3972,879303571429  3967,636857142857             4 1893536970
2025-11-05 09:36:39 XAUUSDm SWING_HIGH         1 3969,7991785714285             3973,7991785714285 3968,8078571428573             4 1893531509
2025-11-05 09:36:09 XAUUSDm SWING_HIGH         1  3969,393092857143              3973,393092857143 3968,4052857142856             4 1893528547
2025-11-05 09:35:38 XAUUSDm SWING_HIGH         1 3969,0596964285714             3973,0596964285714 3968,0471428571427             4 1893525516
2025-11-05 09:34:37 XAUUSDm SWING_HIGH         1        3966,257675                    3970,257675           3965,533             4 1893520552
2025-11-05 09:34:06 XAUUSDm SWING_HIGH         1  3966,995435714286              3970,995435714286 3966,1985714285715             4 1893518566
2025-11-05 09:26:01 XAUUSDm SWING_HIGH         1  3966,256835714286              3970,256835714286 3965,3615714285716             4 1893488903
2025-11-05 09:18:53 XAUUSDm SWING_HIGH         1  3967,038864285714              3971,038864285714 3965,6504285714286             4 1893450321
2025-11-05 09:10:12 XAUUSDm SWING_HIGH        -1 3964,8380428571427             3960,8380428571427 3966,0662857142856             4 1893406279
2025-11-05 09:09:42 XAUUSDm SWING_HIGH        -1        3964,762225                    3960,762225 3965,9829999999997             4 1893404247
2025-11-05 09:09:11 XAUUSDm SWING_HIGH        -1 3964,0111428571427             3960,0111428571427 3965,3582857142856             4 1893401992
2025-11-05 09:08:41 XAUUSDm SWING_HIGH        -1 3963,8254357142855             3959,8254357142855  3965,283571428571             4 1893399889
2025-11-05 09:07:39 XAUUSDm SWING_HIGH        -1 3964,8957714285716             3960,8957714285716  3966,463142857143             4 1893394283
2025-11-05 09:06:09 XAUUSDm SWING_HIGH        -1  3965,114639285714              3961,114639285714 3966,5234285714287             4 1893387428
2025-11-05 09:05:38 XAUUSDm SWING_HIGH        -1  3965,054271428571              3961,054271428571 3966,4781428571428             4 1893384911
2025-11-05 09:05:08 XAUUSDm SWING_HIGH        -1 3965,1201035714284             3961,1201035714284 3966,6738571428573             4 1893380986
2025-11-05 09:04:06 XAUUSDm SWING_HIGH        -1         3965,78445                     3961,78445           3967,242             4 1893377352
2025-11-05 09:03:36 XAUUSDm SWING_HIGH        -1 3966,2910821428572             3962,2910821428572 3967,7227142857146             4 1893375535
2025-11-05 09:03:06 XAUUSDm SWING_HIGH        -1 3966,3672392857143             3962,3672392857143  3967,792428571429             4 1893373125
2025-11-05 09:02:05 XAUUSDm SWING_HIGH        -1 3964,7856107142857             3960,7856107142857 3966,0315714285716             4 1893367950
2025-11-05 09:01:34 XAUUSDm SWING_HIGH        -1 3965,7278035714285             3961,7278035714285 3966,9248571428575             4 1893365438
2025-11-05 09:01:04 XAUUSDm SWING_HIGH        -1  3966,350378571429              3962,350378571429 3967,4828571428575             4 1893363542
2025-11-05 09:00:04 XAUUSDm SWING_HIGH        -1 3965,0618535714284             3961,0618535714284  3966,420857142857             4 1893358707
2025-11-05 08:59:33 XAUUSDm SWING_HIGH        -1  3966,697592857143              3962,697592857143  3967,862285714286             4 1893356741
2025-11-05 08:58:31 XAUUSDm SWING_HIGH        -1          3966,4192                      3962,4192           3967,723             4 1893353285
2025-11-05 08:57:24 XAUUSDm SWING_HIGH        -1  3967,494728571429              3963,494728571429 3968,6538571428573             4 1893348431
2025-11-05 08:56:54 XAUUSDm SWING_HIGH        -1 3967,4889857142857             3963,4889857142857  3968,924571428571             4 1893346196
2025-11-05 08:56:23 XAUUSDm SWING_HIGH        -1        3967,816975                    3963,816975           3969,294             4 1893344390
2025-11-05 08:55:53 XAUUSDm SWING_HIGH        -1 3967,8490535714286             3963,8490535714286  3969,322857142857             4 1893341171
2025-11-05 08:55:22 XAUUSDm SWING_HIGH        -1  3968,249967857143              3964,249967857143 3969,7272857142857             4 1893339132
2025-11-05 08:54:52 XAUUSDm SWING_HIGH        -1        3968,238275                    3964,238275           3969,744             4 1893336394
2025-11-05 08:54:21 XAUUSDm SWING_HIGH        -1 3968,8453642857144             3964,8453642857144 3970,3474285714287             4 1893334567
2025-11-05 08:43:00 XAUUSDm SWING_HIGH         1 3972,7905357142854             3976,7905357142854 3971,4565714285714             4 1893285964
2025-11-05 08:42:30 XAUUSDm SWING_HIGH         1 3972,5398607142856             3976,5398607142856  3971,233571428571             4 1893283931
2025-11-05 08:41:59 XAUUSDm SWING_HIGH         1  3972,928867857143              3976,928867857143  3971,663285714286             4 1893281028
2025-11-05 08:41:28 XAUUSDm SWING_HIGH         1 3972,1387357142858             3976,1387357142858 3970,7965714285715             4 1893277886
2025-11-05 08:40:56 XAUUSDm SWING_HIGH         1  3971,807089285714              3975,807089285714 3970,4504285714283             4 1893274353
2025-11-05 08:40:25 XAUUSDm SWING_HIGH         1 3970,2348142857145             3974,2348142857145 3968,9714285714285             4 1893271854
2025-11-05 08:39:55 XAUUSDm SWING_HIGH         1 3969,8658857142855             3973,8658857142855 3968,4765714285713             4 1893270177
2025-11-05 08:35:07 XAUUSDm SWING_HIGH         1  3971,524432142857              3975,524432142857  3970,235714285714             4 1893248930
2025-11-05 08:34:06 XAUUSDm SWING_HIGH         1 3970,0937035714283             3974,0937035714283  3968,957857142857             4 1893242798
2025-11-05 08:33:34 XAUUSDm SWING_HIGH         1  3969,662428571429              3973,662428571429 3968,5378571428573             4 1893240309
2025-11-05 08:28:27 XAUUSDm SWING_HIGH         1  3968,142057142857              3972,142057142857  3966,622714285714             4 1893216653
2025-11-05 08:27:56 XAUUSDm SWING_HIGH         1 3968,6761428571426             3972,6761428571426 3967,1122857142855             4 1893214874
2025-11-05 08:27:27 XAUUSDm SWING_HIGH         1 3968,8524428571427             3972,8524428571427 3967,1122857142855             4 1893213373
2025-11-05 08:26:55 XAUUSDm SWING_HIGH         1 3969,0634785714287             3973,0634785714287 3967,3218571428574             4 1893211450
2025-11-05 08:25:53 XAUUSDm SWING_HIGH         1 3975,1323231554456             3979,1323231554456 3741,2140737821856             4 1893207338
2025-11-05 08:25:22 XAUUSDm SWING_HIGH         1   3974,55204623674               3978,55204623674 3736,0121505304064             4 1893205323
2025-11-05 08:24:51 XAUUSDm SWING_HIGH         1  3975,183983425558              3979,183983425558  3732,464662977682             4 1893201912
2025-11-05 08:24:20 XAUUSDm SWING_HIGH         1  3974,826911148865              3978,826911148865 3723,0085540454097             4 1893199403
2025-11-05 08:23:50 XAUUSDm SWING_HIGH         1  3973,535351982484              3977,535351982484  3716,122920700646             4 1893196890
2025-11-05 08:23:19 XAUUSDm SWING_HIGH         1  3972,898167965978              3976,898167965978 3710,5732813608856             4 1893194397
2025-11-05 08:22:48 XAUUSDm SWING_HIGH         1 3973,2141894109477             3977,2141894109477 3706,9114235620923             4 1893191978
2025-11-05 08:22:16 XAUUSDm SWING_HIGH         1 3973,1257132337078             3977,1257132337078 3701,1844706516913             4 1893189527
2025-11-05 08:21:45 XAUUSDm SWING_HIGH         1  3975,281380925958              3979,281380925958 3698,3107629616893             4 1893186063
2025-11-05 08:21:11 XAUUSDm SWING_HIGH         1 3972,7976310340878             3976,7976310340878  3691,511758636488             4 1893183384
2025-11-05 08:20:38 XAUUSDm SWING_HIGH         1   3972,05695915713               3976,05695915713  3686,821633714788             4 1893180115
2025-11-05 08:19:39 XAUUSDm SWING_HIGH         1 3973,5407549878855             3977,5407549878855  3683,885800484591             4 1893175805
2025-11-04 22:05:51 XAUUSDm SWING_HIGH        -1 3932,7320785714287             3928,7320785714287  3934,491857142857             4 1891448577
2025-11-04 22:05:45 XAUUSDm SWING_HIGH        -1         3933,09965                     3929,09965           3934,877             4 1891445320
2025-11-04 22:05:09 XAUUSDm SWING_HIGH        -1 3931,5321464285717             3927,5321464285717  3933,084142857143             4 1891441873
2025-11-04 22:04:08 XAUUSDm SWING_HIGH        -1 3933,4915499999997             3929,4915499999997           3934,822             4 1891435823
2025-11-04 22:02:44 XAUUSDm SWING_HIGH        -1  3936,686717857143              3932,686717857143  3937,641285714286             4 1891428331
2025-11-04 22:00:25 XAUUSDm SWING_HIGH        -1 3937,4014357142855             3933,4014357142855  3938,285571428571             4 1891418522
2025-11-04 21:54:06 XAUUSDm SWING_HIGH        -1  3937,521185714286              3933,521185714286 3938,4155714285716             4 1891388750
2025-11-04 21:53:26 XAUUSDm SWING_HIGH        -1  3937,760557142857              3933,760557142857 3938,6397142857145             4 1891386737
2025-11-04 21:51:39 XAUUSDm SWING_HIGH        -1 3937,4536464285716             3933,4536464285716  3938,534142857143             4 1891380968
2025-11-04 21:50:59 XAUUSDm SWING_HIGH        -1  3936,942192857143              3932,942192857143 3938,0412857142856             4 1891378273
2025-11-04 21:50:30 XAUUSDm SWING_HIGH        -1  3937,059389285714              3933,059389285714 3938,1914285714283             4 1891375596
2025-11-04 21:49:54 XAUUSDm SWING_HIGH        -1 3936,6014785714287             3932,6014785714287  3937,688857142857             4 1891372137
2025-11-04 21:49:12 XAUUSDm SWING_HIGH        -1  3937,684432142857              3933,684432142857  3938,691714285714             4 1891368465
2025-11-04 21:46:46 XAUUSDm SWING_HIGH        -1  3937,425410714286              3933,425410714286  3938,597571428572             4 1891358167
2025-11-04 21:46:15 XAUUSDm SWING_HIGH        -1 3936,7753285714284             3932,7753285714284  3937,991857142857             4 1891355940
2025-11-04 21:45:45 XAUUSDm SWING_HIGH        -1        3937,097625                    3933,097625           3938,302             4 1891353167
2025-11-04 21:45:15 XAUUSDm SWING_HIGH        -1 3937,5047285714286             3933,5047285714286 3938,7048571428572             4 1891350856
2025-11-04 21:44:44 XAUUSDm SWING_HIGH        -1  3938,163610714286              3934,163610714286 3939,3685714285716             4 1891347782
2025-11-04 21:41:46 XAUUSDm SWING_HIGH        -1 3940,0011607142856             3936,0011607142856 3941,0605714285716             4 1891328240
2025-11-04 21:41:18 XAUUSDm SWING_HIGH        -1 3940,8140035714287             3936,8140035714287 3941,7568571428574             4 1891325081
2025-11-04 21:40:04 XAUUSDm SWING_HIGH        -1 3941,1086892857143             3937,1086892857143  3942,064428571429             4 1891321134
2025-11-04 21:39:34 XAUUSDm SWING_HIGH        -1 3941,2612714285715             3937,2612714285715  3942,275142857143             4 1891318789
2025-11-04 21:28:56 XAUUSDm SWING_HIGH         1 3942,5566821428574             3946,5566821428574 3941,5447142857142             4 1891263157
2025-11-04 21:28:25 XAUUSDm SWING_HIGH         1  3942,718332142857              3946,718332142857  3941,597714285714             4 1891261274
2025-11-04 21:27:16 XAUUSDm SWING_HIGH         1 3942,5635964285716             3946,5635964285716  3941,268142857143             4 1891256443
2025-11-04 21:25:45 XAUUSDm SWING_HIGH         1  3943,302514285714              3947,302514285714 3942,1334285714283             4 1891250644
2025-11-04 21:25:17 XAUUSDm SWING_HIGH         1 3942,9909428571427             3946,9909428571427  3941,804285714286             4 1891246412
2025-11-04 21:20:57 XAUUSDm SWING_HIGH         1  3941,667114285714              3945,667114285714 3939,5304285714283             4 1891226513
2025-11-04 20:37:37 XAUUSDm SWING_HIGH         1 3941,5224565904546             3945,5224565904546 3756,4297363818127             4 1891002204
2025-11-04 20:37:01 XAUUSDm SWING_HIGH         1  3940,436751689702              3944,436751689702  3749,263932411915             4 1890998940
2025-11-04 20:36:26 XAUUSDm SWING_HIGH         1 3943,9781300989653             3947,9781300989653 3748,1157960413907             4 1890993852
2025-11-04 20:35:54 XAUUSDm SWING_HIGH         1 3946,4808826666776             3950,4808826666776  3746,528693332885             4 1890985152
2025-11-04 20:35:05 XAUUSDm SWING_HIGH         1  3948,413715586736              3952,413715586736 3745,3113765305625             4 1890978710
2025-11-04 20:34:07 XAUUSDm SWING_HIGH         1 3947,7365948448287             3951,7365948448287  3738,735206206865             4 1890973263
2025-11-04 20:33:33 XAUUSDm SWING_HIGH         1 3949,0155614127957             3953,0155614127957  3738,170543488171             4 1890968479
2025-11-04 20:33:06 US30m   SWING_HIGH         1  47238,58333060237              47242,58333060237  40748,96677590536             4 1890964839
2025-11-04 20:33:05 XAUUSDm SWING_HIGH         1  3948,477533672135              3952,477533672135  3732,098653114585             4 1890964652
2025-11-04 20:32:34 US30m   SWING_HIGH         1   47246,4858026607               47250,4858026607  40752,66789357193             4 1890960571
2025-11-04 20:32:32 XAUUSDm SWING_HIGH         1 3951,2625427322846             3955,2625427322846 3728,4872907086146             4 1890960340
2025-11-04 17:00:56 XAUUSDm SWING_HIGH         1 3956,4259357142855             3960,4259357142855 3953,2305714285712             4 1889671889
2025-11-04 17:00:26 XAUUSDm SWING_HIGH         1  3958,035232142857              3962,035232142857  3954,909714285714             4 1889668692
2025-11-04 16:59:55 XAUUSDm SWING_HIGH         1 3957,8245464285715             3961,8245464285715 3954,6451428571427             4 1889664820
2025-11-04 16:59:24 XAUUSDm SWING_HIGH         1 3957,6437571428573             3961,6437571428573  3954,414714285714             4 1889660152
2025-11-04 16:58:54 XAUUSDm SWING_HIGH         1 3956,3722857142857             3960,3722857142857 3953,2445714285714             4 1889656003
2025-11-04 16:58:23 XAUUSDm SWING_HIGH         1 3954,4744357142854             3958,4744357142854 3951,4635714285714             4 1889652044
2025-11-04 16:57:22 XAUUSDm SWING_HIGH         1  3951,576407142857              3955,576407142857 3948,8127142857143             4 1889646290
2025-11-04 16:56:50 XAUUSDm SWING_HIGH         1 3953,1330035714286             3957,1330035714286  3950,508857142857             4 1889642712
2025-11-04 16:56:20 XAUUSDm SWING_HIGH         1         3953,74185                     3957,74185            3950,96             4 1889639408
2025-11-04 16:55:48 XAUUSDm SWING_HIGH         1         3953,52515                     3957,52515           3950,567             4 1889635497
2025-11-04 16:55:16 XAUUSDm SWING_HIGH         1 3951,0846464285714             3955,0846464285714  3948,352142857143             4 1889631057
2025-11-04 16:45:38 XAUUSDm SWING_HIGH        -1 3935,0967178571427             3931,0967178571427 3939,3722857142857             4 1889556982
2025-11-04 16:45:06 XAUUSDm SWING_HIGH        -1 3933,8140785714286             3929,8140785714286 3937,9928571428572             4 1889552130
2025-11-04 16:44:36 XAUUSDm SWING_HIGH        -1  3933,454796428571              3929,454796428571  3938,137142857143             4 1889546168
2025-11-04 16:43:35 XAUUSDm SWING_HIGH        -1  3934,337728571428              3930,337728571428  3938,940857142857             4 1889536016
2025-11-04 16:42:34 XAUUSDm SWING_HIGH        -1 3933,0889392857143             3929,0889392857143 3936,5764285714286             4 1889524217
2025-11-04 16:38:10 XAUUSDm SWING_HIGH        -1 3938,1899785714286             3934,1899785714286 3941,9628571428575             4 1889470626
2025-11-04 16:37:41 XAUUSDm SWING_HIGH        -1 3937,5551499999997             3933,5551499999997           3941,772             4 1889463799
2025-11-04 16:37:09 XAUUSDm SWING_HIGH        -1 3941,3456464285714             3937,3456464285714  3945,378142857143             4 1889458595
2025-11-04 16:36:32 XAUUSDm SWING_HIGH        -1 3938,8365035714287             3934,8365035714287 3944,5558571428573             4 1889451601
2025-11-04 16:36:01 XAUUSDm SWING_HIGH        -1  3936,332342857143              3932,332342857143 3941,7302857142854             4 1889443652
2025-11-04 16:35:30 XAUUSDm SWING_HIGH        -1  3936,224867857143              3932,224867857143 3941,7652857142857             4 1889439138
2025-11-04 16:35:00 XAUUSDm SWING_HIGH        -1  3937,147932142857              3933,147932142857 3942,6037142857144             4 1889431582
2025-11-04 16:34:30 XAUUSDm SWING_HIGH        -1 3937,4931714285717             3933,4931714285717  3942,939142857143             4 1889423122
2025-11-04 16:33:58 XAUUSDm SWING_HIGH        -1 3941,3779000000004             3937,3779000000004           3946,425             4 1889414063
2025-11-04 16:33:28 XAUUSDm SWING_HIGH        -1 3943,4507928571425             3939,4507928571425 3948,5432857142855             4 1889406716
2025-11-04 16:32:56 XAUUSDm SWING_HIGH        -1        3945,707975                    3941,707975           3950,547             4 1889397642
2025-11-04 16:32:21 XAUUSDm SWING_HIGH        -1          3949,0585                      3945,0585 3953,5480000000002             4 1889388727
2025-11-04 16:31:48 XAUUSDm SWING_HIGH        -1 3951,5307285714284             3947,5307285714284  3955,723857142857             4 1889378314
2025-11-04 16:31:05 XAUUSDm SWING_HIGH        -1  3952,000785714286              3948,000785714286 3956,3145714285715             4 1889369386
2025-11-04 16:30:37 XAUUSDm SWING_HIGH        -1  3952,525207142857              3948,525207142857  3956,903714285714             4 1889363346
2025-11-04 16:30:06 XAUUSDm SWING_HIGH        -1 3956,1925892857143             3952,1925892857143  3960,104428571429             4 1889356931
2025-11-04 16:28:20 XAUUSDm SWING_HIGH        -1        3967,387875                    3963,387875 3969,1969999999997             4 1889323261
2025-11-04 16:27:27 XAUUSDm SWING_HIGH        -1 3968,4609107142855             3964,4609107142855 3970,4325714285715             4 1889319415
2025-11-04 16:27:03 XAUUSDm SWING_HIGH        -1          3968,8039                      3964,8039           3970,776             4 1889314801
2025-11-04 16:26:31 XAUUSDm SWING_HIGH        -1  3969,079110714286              3965,079110714286 3971,1655714285716             4 1889312560
2025-11-04 16:25:47 XAUUSDm SWING_HIGH        -1 3970,2307142857144             3966,2307142857144 3972,2924285714284             4 1889309604
2025-11-04 16:10:07 XAUUSDm SWING_HIGH        -1         3970,13085                     3966,13085           3971,408             4 1889202165
2025-11-04 16:06:58 XAUUSDm SWING_HIGH        -1 3970,8458250000003             3966,8458250000003 3972,9030000000002             4 1889181786
2025-11-04 16:06:22 XAUUSDm SWING_HIGH        -1 3969,7336642857144             3965,7336642857144 3971,6744285714285             4 1889176179
2025-11-04 16:05:29 XAUUSDm SWING_HIGH        -1  3968,498928571428              3964,498928571428  3970,346857142857             4 1889162366
2025-11-04 16:04:42 XAUUSDm SWING_HIGH        -1 3969,7393142857145             3965,7393142857145 3971,4074285714287             4 1889156018
2025-11-04 16:04:10 XAUUSDm SWING_HIGH        -1  3969,060692857143              3965,060692857143  3970,795285714286             4 1889151264
2025-11-04 16:02:52 XAUUSDm SWING_HIGH        -1         3970,30155                     3966,30155           3971,878             4 1889140763
2025-11-04 16:02:34 XAUUSDm SWING_HIGH        -1 3970,1736928571427             3966,1736928571427 3971,9902857142856             4 1889135606
2025-11-04 16:01:55 XAUUSDm SWING_HIGH        -1 3970,1992214285715             3966,1992214285715 3972,5271428571427             4 1889131167
2025-11-04 16:01:06 XAUUSDm SWING_HIGH        -1 3971,2925642857144             3967,2925642857144 3973,4834285714282             4 1889125357
2025-11-04 16:00:00 XAUUSDm SWING_HIGH        -1  3975,396453571429              3971,396453571429  3977,304857142857             4 1889109353
2025-11-04 15:59:35 XAUUSDm SWING_HIGH        -1 3976,0422249999997             3972,0422249999997           3978,124             4 1889104705
2025-11-04 15:59:04 XAUUSDm SWING_HIGH        -1  3977,242157142857              3973,242157142857  3979,285714285714             4 1889101921
2025-11-04 15:57:30 XAUUSDm SWING_HIGH        -1         3976,24225                     3972,24225           3978,446             4 1889092589
2025-11-04 15:54:18 XAUUSDm SWING_HIGH        -1  3975,102492857143              3971,102492857143  3977,337285714286             4 1889071366
2025-11-04 15:53:14 XAUUSDm SWING_HIGH        -1  3975,307221428571              3971,307221428571  3977,512142857143             4 1889064956
2025-11-04 15:50:44 XAUUSDm SWING_HIGH        -1  3976,494435714286              3972,494435714286 3978,2805714285714             4 1889045294
2025-11-04 15:50:03 XAUUSDm SWING_HIGH        -1  3976,648057142857              3972,648057142857 3978,4497142857144             4 1889031883
2025-11-04 15:48:09 XAUUSDm SWING_HIGH        -1  3978,811407142857              3974,811407142857 3980,8037142857142             4 1889016266
2025-11-04 15:45:33 XAUUSDm SWING_HIGH        -1 3980,0588357142856             3976,0588357142856 3982,7305714285712             4 1888994226
2025-11-04 15:40:48 XAUUSDm SWING_HIGH        -1 3981,1893250000003             3977,1893250000003           3985,153             4 1888957059
2025-11-04 15:39:41 XAUUSDm SWING_HIGH        -1          3978,3784                      3974,3784           3981,929             4 1888949618
2025-11-04 15:38:09 XAUUSDm SWING_HIGH        -1  3979,286692857143              3975,286692857143 3982,1692857142857             4 1888925684
2025-11-04 15:37:11 XAUUSDm SWING_HIGH        -1 3982,0555464285712             3978,0555464285712  3984,534142857143             4 1888919536
2025-11-04 15:35:49 XAUUSDm SWING_HIGH        -1  3980,232082142857              3976,232082142857 3982,4427142857144             4 1888907869
2025-11-04 15:35:08 XAUUSDm SWING_HIGH        -1  3979,046332142857              3975,046332142857 3981,0827142857142             4 1888897528
2025-11-04 15:33:33 XAUUSDm SWING_HIGH        -1 3985,3792857142857             3981,3792857142857 3986,5155714285715             4 1888875270
2025-11-04 15:32:05 XAUUSDm SWING_HIGH        -1 3986,8884749999997             3982,8884749999997           3987,976             4 1888870521
2025-11-04 15:25:47 XAUUSDm SWING_HIGH        -1  3987,159214285714              3983,159214285714 3987,6424285714284             4 1888852593
2025-11-04 15:19:40 XAUUSDm SWING_HIGH         1 3993,2705178571427             3997,2705178571427  3992,060285714286             4 1888747569
2025-11-04 15:17:00 XAUUSDm SWING_HIGH         1 3994,4519214285715             3998,4519214285715 3993,0201428571427             4 1888726788
2025-11-04 15:16:02 XAUUSDm SWING_HIGH         1  3992,812246428571              3996,812246428571 3991,4081428571426             4 1888719903
2025-11-04 15:15:18 XAUUSDm SWING_HIGH         1  3993,593835714286              3997,593835714286 3992,2065714285714             4 1888713785
2025-11-04 15:13:00 XAUUSDm SWING_HIGH         1 3994,6258714285714             3998,6258714285714  3993,155142857143             4 1888697164
2025-11-04 15:12:29 XAUUSDm SWING_HIGH         1  3993,565417857143              3997,565417857143  3992,113285714286             4 1888692953
2025-11-04 15:11:02 XAUUSDm SWING_HIGH         1  3992,678632142857              3996,678632142857 3991,3407142857145             4 1888681099
2025-11-04 15:00:54 XAUUSDm SWING_HIGH        -1           3985,575                       3981,575 3986,8869999999997             4 1888605152
2025-11-04 15:00:03 XAUUSDm SWING_HIGH        -1  3984,925607142857              3980,925607142857 3986,2537142857145             4 1888599494
2025-11-04 14:59:44 XAUUSDm SWING_HIGH        -1 3984,9473857142857             3980,9473857142857  3986,366571428571             4 1888595384
2025-11-04 14:59:00 XAUUSDm SWING_HIGH        -1  3985,331442857143              3981,331442857143  3986,953285714286             4 1888590866
2025-11-04 14:58:21 XAUUSDm SWING_HIGH        -1 3985,7117642857143             3981,7117642857143 3987,2794285714285             4 1888587743
2025-11-04 14:57:33 XAUUSDm SWING_HIGH        -1 3986,4222357142858             3982,4222357142858  3987,888571428571             4 1888584137
2025-11-04 14:56:41 XAUUSDm SWING_HIGH        -1          3985,0394                      3981,0394           3986,458             4 1888577258
2025-11-04 14:55:57 XAUUSDm SWING_HIGH        -1 3984,8095321428573             3980,8095321428573  3986,304714285714             4 1888572063
2025-11-04 14:55:17 XAUUSDm SWING_HIGH        -1 3984,5171464285713             3980,5171464285713 3985,9871428571423             4 1888566357
2025-11-04 14:54:34 XAUUSDm SWING_HIGH        -1 3985,9296178571426             3981,9296178571426 3987,3392857142853             4 1888560963
2025-11-04 14:52:40 XAUUSDm SWING_HIGH        -1  3988,173792857143              3984,173792857143 3989,5352857142852             4 1888545170
2025-11-04 14:52:02 XAUUSDm SWING_HIGH        -1 3987,4140607142854             3983,4140607142854  3988,805571428571             4 1888541942
2025-11-04 14:50:01 XAUUSDm SWING_HIGH        -1         3988,54655                     3984,54655 3989,7129999999997             4 1888529093
2025-11-04 14:49:34 XAUUSDm SWING_HIGH        -1         3988,55555                     3984,55555 3989,7219999999998             4 1888525350
2025-11-04 14:21:38 XAUUSDm SWING_HIGH         1 3996,1559785714285             4000,1559785714285 3995,3368571428573             4 1888311936
2025-11-04 14:17:28 XAUUSDm SWING_HIGH         1 3996,6064714285717             4000,6064714285717 3995,9311428571427             4 1888302630
2025-11-04 14:13:32 XAUUSDm SWING_HIGH        -1 3994,7008857142855             3990,7008857142855 3995,4025714285713             4 1888269630
2025-11-04 14:12:50 XAUUSDm SWING_HIGH        -1        3995,021425                    3991,021425           3995,701             4 1888265902
2025-11-04 14:11:51 XAUUSDm SWING_HIGH        -1 3994,7781714285716             3990,7781714285716 3995,6321428571428             4 1888259425
2025-11-04 14:11:02 XAUUSDm SWING_HIGH        -1 3994,3339928571427             3990,3339928571427 3995,1542857142854             4 1888255747
2025-11-04 14:10:35 XAUUSDm SWING_HIGH        -1 3994,7428214285715             3990,7428214285715  3995,570142857143             4 1888251969
2025-11-04 14:09:22 XAUUSDm SWING_HIGH         1 3995,3057785714286             3999,3057785714286 3994,2898571428573             4 1888247312
2025-11-04 14:08:53 XAUUSDm SWING_HIGH         1 3995,6787785714287             3999,6787785714287 3994,7038571428575             4 1888245391
2025-11-04 14:08:21 XAUUSDm SWING_HIGH         1 3995,5406428571428             3999,5406428571428  3994,530285714286             4 1888243340
2025-11-04 14:07:38 XAUUSDm SWING_HIGH         1 3995,9989035714284             3999,9989035714284  3994,936857142857             4 1888240148
2025-11-04 14:05:41 XAUUSDm SWING_HIGH         1 3995,4915928571427             3999,4915928571427  3994,442285714286             4 1888231000
2025-11-04 14:04:10 XAUUSDm SWING_HIGH         1 3995,5660535714283             3999,5660535714283  3994,374857142857             4 1888223302
2025-11-04 14:03:41 XAUUSDm SWING_HIGH         1 3995,7816357142856             3999,7816357142856 3994,5665714285715             4 1888220953
2025-11-04 13:54:41 XAUUSDm SWING_HIGH         1        3995,540525                    3999,540525           3993,756             4 1888169096
2025-11-04 13:53:39 XAUUSDm SWING_HIGH         1  3997,071553571429              4001,071553571429 3995,3678571428577             4 1888163014
2025-11-04 13:52:46 XAUUSDm SWING_HIGH         1 3997,3973464285714             4001,3973464285714  3995,661142857143             4 1888159338
2025-11-04 13:51:32 XAUUSDm SWING_HIGH         1  3998,298864285714              4002,298864285714 3996,6234285714286             4 1888151705
2025-11-04 13:50:54 XAUUSDm SWING_HIGH         1  3999,307128571428              4003,307128571428  3997,743857142857             4 1888147160
2025-11-04 11:50:04 XAUUSDm SWING_HIGH         1 4000,1801885552663             4004,1801885552663 3741,5854577893424             4 1887520734
2025-11-04 11:50:04 US30m   SWING_HIGH         1  47139,50218015249              47143,50218015249  40587,61279390009             4 1887520764
2025-11-04 11:49:33 XAUUSDm SWING_HIGH         1 4001,6392749766724             4005,6392749766724 3736,1120009331103             4 1887517545
2025-11-04 11:49:33 US30m   SWING_HIGH         1 47152,179996565756             47156,179996565756  40597,10013736994             4 1887517592
2025-11-04 11:49:03 XAUUSDm SWING_HIGH         1   4001,46461200058               4005,46461200058 3727,7645199768017             4 1887514023
2025-11-04 11:49:02 US30m   SWING_HIGH         1  47149,78324817868              47153,78324817868  40590,47007285279             4 1887514120
2025-11-04 11:48:32 XAUUSDm SWING_HIGH         1  4000,646785066806              4004,646785066806 3723,9465973277674             4 1887511314
2025-11-04 11:48:32 US30m   SWING_HIGH         1  47142,21380502946              47146,21380502946  40581,64779882136             4 1887511363
