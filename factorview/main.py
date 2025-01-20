import numpy as np
import pandas as pd
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .data_loader import (
    load_factor_info,
    load_factor_perf,
    load_factor_stats,
    load_factor_stats_backtest,
    load_factor_stats_group,
    load_factor_stats_ic,
    load_factor_update_info,
    load_strategy_factor_stats,
    load_strategy_info,
    load_strategy_perf,
)

app = FastAPI()

# 允许所有来源的跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有HTTP方法
    allow_headers=["*"],  # 允许所有请求头
)


def clean_for_json(data):
    if isinstance(data, pd.DataFrame):
        return {c: clean_for_json(data[c]) for c in data.columns}
    if isinstance(data, (list, tuple, pd.Index, pd.Series, np.ndarray)):
        return [clean_for_json(x) for x in data]
    elif isinstance(data, dict):
        return {k: clean_for_json(v) for k, v in data.items()}
    elif isinstance(data, (float, int)):
        return None if pd.isna(data) else data
    if isinstance(data, pd.Timestamp):
        return data.strftime(r"%Y-%m-%d")
    return data


@app.get("/api/factor")
async def get_factor_info(
    factor_names: list[str] = Query(None),
    table_names: list[str] = Query(None),
    class_names: list[str] = Query(None),
    status: list[str] = Query(None),
    develop_codes: list[str] = Query(None),
    factor_ids: list[str] = Query(None),
    creation_time: list[str] = Query(None),
):
    """取因子基本信息"""
    factor_info = load_factor_info(
        factor_names=factor_names,
        table_names=table_names,
        class_names=class_names,
        status=status,
        develop_codes=develop_codes,
        factor_ids=factor_ids,
        creation_time=creation_time,
    )
    return JSONResponse(
        {
            "factor_info": {
                "values": clean_for_json(factor_info),
                "index": clean_for_json(factor_info.index),
            }
        }
    )


@app.get("/api/factor/stats")
async def get_factor_stats(
    factor_names: list[str] = Query(default=None, alias="factor_names[]"),
    start_date: str = Query(None),
    end_date: str = Query(None),
    pool: str = Query("all"),
    optimizer_index: str = Query("000905.SH"),
    benchmark_index: str = Query("000905.SH"),
):
    """取因子统计信息"""
    factor_stats = load_factor_stats(
        factor_names=factor_names,
        start_date=start_date,
        end_date=end_date,
        pool=pool,
        optimizer_index=optimizer_index,
        benchmark_index=benchmark_index,
    )
    return JSONResponse(
        {
            name: {
                "values": clean_for_json(df),
                "index": clean_for_json(df.index),
            }
            for name, df in zip(
                ["factor_info", "ic", "group", "backtest_ret", "date"],
                factor_stats,
            )
        }
    )


@app.get("/api/factor/stats/backtest")
async def get_factor_stats_backtest(
    factor_names: list[str] = Query(default=None, alias="factor_names[]"),
    start_date: str = Query(None),
    end_date: str = Query(None),
    pool: str = Query("all"),
    optimizer_index: str = Query("000905.SH"),
    benchmark_index: str = Query("000905.SH"),
):
    """取因子回测统计信息"""

    backtest_dict = load_factor_stats_backtest(
        factor_names=factor_names,
        start_date=start_date,
        end_date=end_date,
        pool=pool,
        optimizer_index=optimizer_index,
        benchmark_index=benchmark_index,
    )
    return JSONResponse(
        {
            name: {
                "values": clean_for_json(df),
                "index": clean_for_json(df.index),
            }
            for name, df in backtest_dict.items()
        }
    )


@app.get("/api/factor/stats/group")
async def get_factor_stats_group(
    factor_names: list[str] = Query(default=None, alias="factor_names[]"),
    start_date: str = Query(None),
    end_date: str = Query(None),
    pool: str = Query("all"),
    optimizer_index: str = Query("000905.SH"),
    benchmark_index: str = Query("000905.SH"),
):
    """取因子分组统计信息"""

    group_dict = load_factor_stats_group(
        factor_names=factor_names,
        start_date=start_date,
        end_date=end_date,
        pool=pool,
        optimizer_index=optimizer_index,
        benchmark_index=benchmark_index,
    )
    return JSONResponse(
        {
            name: {
                "values": clean_for_json(df),
                "index": clean_for_json(df.index),
            }
            for name, df in group_dict.items()
        }
    )


@app.get("/api/factor/stats/ic")
async def get_factor_stats_ic(
    factor_names: list[str] = Query(default=None, alias="factor_names[]"),
    start_date: str = Query(None),
    end_date: str = Query(None),
    pool: str = Query("all"),
    optimizer_index: str = Query("000905.SH"),
    benchmark_index: str = Query("000905.SH"),
):
    """取因子IC统计信息"""

    ic_dict = load_factor_stats_ic(
        factor_names=factor_names,
        start_date=start_date,
        end_date=end_date,
        pool=pool,
        optimizer_index=optimizer_index,
        benchmark_index=benchmark_index,
    )
    return JSONResponse(
        {
            name: {
                "values": clean_for_json(df),
                "index": clean_for_json(df.index),
            }
            for name, df in ic_dict.items()
        }
    )


@app.get("/api/factor/update")
async def get_factor_update(
    factor_names: list[str] = Query(default=None, alias="factor_names[]"),
    start_date: str = Query(None),
    end_date: str = Query(None),
):
    """取因子更新信息"""

    factor_update_info = load_factor_update_info(
        factor_names=factor_names,
        start_date=start_date,
        end_date=end_date,
    )
    return JSONResponse(
        {
            name: clean_for_json(factor_update_info.loc[name].to_dict())
            for name in factor_update_info.index
        }
    )


@app.get("/api/factor/{factor_name}")
async def get_factor_perf(
    factor_name: str,
    start_date: str = Query(None),
    end_date: str = Query(None),
    pool: str = Query("all"),
    optimizer_index: str = Query("000905.SH"),
    benchmark_index: str = Query("000905.SH"),
):
    """取单个因子的表现"""
    factor_perf = load_factor_perf(
        factor_name=factor_name,
        start_date=start_date,
        end_date=end_date,
        pool=pool,
        optimizer_index=optimizer_index,
        benchmark_index=benchmark_index,
    )
    return JSONResponse(
        {
            name: {
                "values": clean_for_json(df.values),
                "index": clean_for_json(df.index),
            }
            for name, df in zip(
                ["ic", "group", "backtest_ret"],
                factor_perf,
            )
        }
    )


@app.get("/api/strategy")
async def get_strategy_info(
    pool: str = Query("all"),
    optimizer_index: str = Query("000905.SH"),
    benchmark_index: str = Query("000905.SH"),
):
    """取策略基本信息"""
    strategy_info = load_strategy_info(
        pool=pool,
        optimizer_index=optimizer_index,
        benchmark_index=benchmark_index,
    )
    return JSONResponse(
        {
            "strategy_info": {
                "values": clean_for_json(strategy_info),
                "index": clean_for_json(strategy_info.index),
            }
        }
    )


@app.get("/api/strategy/{strategy_name}")
async def get_strategy_perf(
    strategy_name: str,
    start_date: str = Query(None),
    end_date: str = Query(None),
    pool: str = Query("all"),
    optimizer_index: str = Query("000905.SH"),
    benchmark_index: str = Query("000905.SH"),
):
    """取单个策略的表现"""
    (backtest_df,) = load_strategy_perf(
        strategy_name=strategy_name,
        start_date=start_date,
        end_date=end_date,
        pool=pool,
        optimizer_index=optimizer_index,
        benchmark_index=benchmark_index,
    )
    return JSONResponse(
        {
            "backtest_ret": {
                "values": clean_for_json(backtest_df.values),
                "index": clean_for_json(backtest_df.index),
            }
        }
    )


@app.get("/api/strategy/{strategy_name}/factors")
async def get_strategy_factors(
    strategy_name: str,
    start_date: str = Query(None),
    end_date: str = Query(None),
    pool: str = Query("all"),
    optimizer_index: str = Query("000905.SH"),
    benchmark_index: str = Query("000905.SH"),
):
    """取策略的统计表现"""
    factor_stats = load_strategy_factor_stats(
        strategy_name=strategy_name,
        start_date=start_date,
        end_date=end_date,
        pool=pool,
        optimizer_index=optimizer_index,
        benchmark_index=benchmark_index,
    )
    return JSONResponse(
        {
            name: {
                "values": clean_for_json(df),
                "index": clean_for_json(df.index),
            }
            for name, df in zip(
                ["factor_info", "ic", "group", "backtest_ret", "date"],
                factor_stats,
            )
        }
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000)
