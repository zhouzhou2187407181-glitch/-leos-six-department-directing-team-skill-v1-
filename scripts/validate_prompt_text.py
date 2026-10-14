#!/usr/bin/env python3
"""Validate the final plain-text video prompt format and 5000-character cap."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


SHOT_PATTERN = re.compile(r"【镜头(\d+)】")
DECLARED_PATTERN = re.compile(r"本视频严格只有\s*(\d+)\s*个镜头")
REQUIRED_GLOBAL = ("⚠️空间布局", "⚠️对白规则：", "环境活动：", "风格：")
REQUIRED_SHOT = ("机位：", "摄影机运动：", "摄影机位置：", "背景：", "动作：", "微表演细节")


def strip_fence(text: str) -> str:
    stripped = text.strip()
    if stripped.startswith("```text") and stripped.endswith("```"):
        return stripped[len("```text") : -3].strip()
    return stripped


def effective_chars(text: str) -> int:
    return sum(1 for char in text if not char.isspace())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt_file", type=Path)
    parser.add_argument("--max-chars", type=int, default=5000)
    args = parser.parse_args()

    try:
        prompt = strip_fence(args.prompt_file.read_text(encoding="utf-8"))
    except (OSError, UnicodeError) as exc:
        print(f"INVALID: 无法读取 UTF-8 提示词: {exc}", file=sys.stderr)
        return 1

    errors: list[str] = []
    warnings: list[str] = []
    count = effective_chars(prompt)

    if not prompt:
        errors.append("提示词为空")
    if prompt.lstrip().startswith(("{", "[")):
        errors.append("最终提示词不得使用 JSON 格式")
    if count > args.max_chars:
        errors.append(f"有效字符 {count}，超过上限 {args.max_chars}")
    if "15秒。16:9" in prompt or "15 秒。16:9" in prompt:
        errors.append("检测到旧版固定时长/画幅结尾")

    for marker in REQUIRED_GLOBAL:
        if marker not in prompt:
            errors.append(f"缺少全局字段: {marker}")

    shot_matches = list(SHOT_PATTERN.finditer(prompt))
    shot_numbers = [int(match.group(1)) for match in shot_matches]
    if not shot_numbers:
        errors.append("未找到【镜头N】结构")
    else:
        expected = list(range(1, len(shot_numbers) + 1))
        if shot_numbers != expected:
            errors.append(f"镜头编号必须连续且不重复，当前为 {shot_numbers}")

        declared = DECLARED_PATTERN.search(prompt)
        if not declared:
            errors.append("缺少明确的镜头总数声明")
        elif int(declared.group(1)) != len(shot_numbers):
            errors.append(f"声明 {declared.group(1)} 镜，与实际 {len(shot_numbers)} 镜不一致")

        for index, match in enumerate(shot_matches):
            end = shot_matches[index + 1].start() if index + 1 < len(shot_matches) else len(prompt)
            block = prompt[match.start() : end]
            for marker in REQUIRED_SHOT:
                if marker not in block:
                    errors.append(f"镜头{shot_numbers[index]}缺少字段: {marker}")

        first_shot = shot_matches[0].start()
        environment = prompt.find("环境活动：", first_shot)
        shot_end = environment if environment >= 0 else len(prompt)
        preamble_ratio = effective_chars(prompt[:first_shot]) / max(count, 1)
        shot_ratio = effective_chars(prompt[first_shot:shot_end]) / max(count, 1)
        if preamble_ratio > 0.25:
            warnings.append(f"资产与空间占比 {preamble_ratio:.0%}，建议继续压缩")
        if shot_ratio < 0.55:
            warnings.append(f"逐镜内容占比 {shot_ratio:.0%}，建议把更多字数留给镜头")

    for warning in warnings:
        print(f"WARNING: {warning}")
    if errors:
        for error in errors:
            print(f"INVALID: {error}", file=sys.stderr)
        return 1

    print(f"VALID: {count}/{args.max_chars} effective characters; {len(shot_numbers)} shots")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
