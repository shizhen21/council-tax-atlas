# 发布 Council Tax Atlas：GitHub Desktop + GitHub Pages

截至 2026-10-29，网站仍是本地预览，没有上传或公开发布。

## 发布哪个文件夹

只选择以下网站文件夹：

`/Users/shizhenwang/Desktop/Council Tax Inequality/11_Website/council-tax-atlas`

必须保留根目录的 index.html、reform-map.html、.nojekyll，以及 assets、data、downloads 文件夹。不要把整个 Council Tax Inequality 研究项目作为网站仓库。

## 第一次发布

1. 在 GitHub Desktop 登录你的 GitHub 账号。
2. 选择 File → Add Local Repository，定位到上面的 council-tax-atlas 文件夹。
3. 如果提示不是 Git repository，点击提示中的 create a repository here，在这个文件夹创建仓库；仓库名用 council-tax-atlas。如果已经识别到仓库，直接添加即可。
4. 如果 Changes 中有未提交的网站文件，在 Summary 填 Initial website，然后 Commit to main（实际分支名以界面为准）。
5. 点击 Publish repository。使用 GitHub Free 的公开 Pages 方案时取消勾选 Keep this code private，确认仓库名后发布。此步骤会公开网站代码与文件夹内的聚合数据。
6. 点击 Repository → View on GitHub，打开仓库网页。
7. 进入 Settings → Pages。在 Build and deployment 下，Source 选 Deploy from a branch；Branch 选 main（或实际已上传的分支）；Folder 选 /(root)，然后 Save。
8. 等待部署完成。Pages 页面会显示真正的网站网址，通常形如 https://你的用户名.github.io/council-tax-atlas/。以页面实际显示的地址为准。
9. 打开网址，检查历史年份、地区搜索、改革原始 band 查询、改革地图和附录；然后把该公开网址放进发给 Sofie 的邮件。

## 后续更新

继续修改同一网站文件夹。GitHub Desktop → Changes → 写更新说明 → Commit to main → Push origin。Pages 会根据所选分支重新部署。不会自动读取本地未推送的修改。

## 为什么不推荐这次直接拖拽上传

当前完整网站约 460 MB，含 1,700 多个 JSON 数据文件；最大下载约 34 MB。Netlify 官方说明拖拽部署在小于 50 MB 时最可靠，超过 10 MB 的单文件可能卡住。Cloudflare Pages 仪表盘拖拽上传有 1,000 文件、每文件 25 MiB 的限制。当前版本使用 GitHub Desktop 上传再开 Pages 更合适；Pages 发布站点上限 1 GB，GitHub 单文件硬上限 100 MB。

如果 Desktop 检测为其他研究项目的大仓库，先不要发布那个仓库；应把网站作为独立仓库处理。

## 官方说明

- https://docs.github.com/en/desktop/adding-and-cloning-repositories/adding-a-repository-from-your-local-computer-to-github-desktop
- https://docs.github.com/en/desktop/overview/creating-your-first-repository-using-github-desktop
- https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site
- https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits

无需购买域名或执行 Git/Node 命令。公开网址部署成功后，Sofie 可在自己的电脑上访问；127.0.0.1 地址仍然只用于你的本地预览。
