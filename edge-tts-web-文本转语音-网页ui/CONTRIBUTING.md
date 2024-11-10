# 贡献指南

感谢您对项目的关注！我们欢迎任何形式的贡献。

## 贡献方式

1. 提交 Issue
- 报告 Bug
- 提出新功能建议
- 改进建议

2. 提交 Pull Request
- 修复 Bug
- 添加新功能
- 改进文档
- 优化性能

## 开发流程

1. Fork 项目
2. 创建特性分支
```bash
git checkout -b feature/your-feature
```

3. 提交更改
```bash
git commit -am 'Add some feature'
```

4. 推送到分支
```bash
git push origin feature/your-feature
```

5. 创建 Pull Request

## 代码规范

1. Python 代码风格
- 遵循 PEP 8 规范
- 使用 4 空格缩进
- 最大行长度 120 字符

2. 注释规范
- 使用中文注释
- 关键逻辑必须添加注释
- 使用 docstring 描述函数功能

3. 提交信息规范
```
feat: 添加新功能
fix: 修复问题
docs: 更新文档
style: 代码格式调整
refactor: 代码重构
test: 添加测试
chore: 其他更改
```

## 测试规范

1. 单元测试
- 使用 pytest 框架
- 测试覆盖率要求 > 80%
- 运行测试：
```bash
pytest tests/
```

2. 代码检查
```bash
# 运行 pylint
pylint app.py

# 运行 mypy 类型检查
mypy app.py
```

## 文档维护

1. 更新文档
- README.md - 项目概述
- INSTALL.md - 安装说明
- CONTRIBUTING.md - 贡献指南
- CHANGELOG.md - 更新日志

2. 文档格式
- 使用 Markdown 格式
- 保持结构清晰
- 示例代码完整

## 版本发布

1. 版本号规范
- 主版本号：不兼容的 API 修改
- 次版本号：向下兼容的功能性新增
- 修订号：向下兼容的问题修正

2. 发布流程
- 更新版本号
- 更新 CHANGELOG.md
- 创建发布标签
- 发布 Release

## 联系方式

- Issue 讨论
- 邮件联系：your-email@example.com
- 开发群：xxx 