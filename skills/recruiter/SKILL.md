---
name: recruiter
description: "Help recruiters publish job postings to the job matching system. Use when users want to: (1) post a job, (2) publish a position, (3) hire someone, (4) recruit candidates, (5) find employees, or (6) advertise job openings. Supports flexible information collection - users can provide all details at once or be guided through step-by-step. Automatically creates recruiter account, generates job vectors, and enables AI-powered candidate matching."
---

# Recruiter

Publish, update, and manage job postings in the AI-powered job matching system, and view matched candidates.

## Overview

This skill helps recruiters manage job postings through an interactive conversation. Provide information flexibly - share everything at once or answer questions step-by-step. The system supports:

1. **Publish job** - Create a recruiter account, publish a job posting, and trigger AI matching
2. **Update job** - Modify job details (title, requirements, salary, etc.)
3. **Delete job** - Soft-delete job posting (mark as INACTIVE, preserving match history)
4. **View jobs** - Check all your published jobs
5. **List matched candidates** - View candidates matched by the AI system with similarity scores

## Available Scripts

- **publish_job.py** - Publish, update, delete jobs, and list matches for a specific job
- **get_profile.py** - View all your jobs and matched candidates (read-only)

## Workflow

### Publish Job (action: publish)

#### Step 1: Gather Job Posting Information

Collect the following required fields. Users can provide them in any order or all at once:

**Required fields:**

- **Job title**: Position name (e.g., "Senior Python Backend Engineer")
- **Company name**: Employer name
- **Job requirements**: Detailed requirements including skills, responsibilities, and qualifications
- **Salary range**: Compensation range (e.g., "25k-40k", "30k-50k")
- **Work location**: Office location (e.g., "Shanghai-Changning District", "Beijing-Chaoyang District")
- **Job type**: Employment type (e.g., "Full-time", "Part-time", "Contract")
- **Education requirement**: Minimum education level (e.g., "Bachelor's degree or above")
- **Experience requirement**: Required years of experience (e.g., "3-5 years", "5+ years")

**Example user inputs:**

_All at once:_

> "I want to post a job for a Python Backend Engineer at Pinduoduo in Shanghai Changning District. Salary 25k-40k. Requirements: Familiar with Python, Django/Flask frameworks, RESTful API development experience. Knowledge of MySQL, Redis databases. E-commerce or payment system experience preferred. Full-time position, bachelor's degree or above, 3-5 years experience."

_Step by step:_

> "I need to hire a developer"
> [Claude asks for job title]
> "Python Backend Engineer"
> [Claude asks for company, requirements, salary, location, etc.]

#### Step 2: Validate Completeness

Before submission, verify all required fields are present. If any are missing, ask the user to provide them.

#### Step 3: Publish Job Posting

```bash
cat <<EOF | python3 scripts/publish_job.py
{
  "action": "publish",
  "title": "<job title>",
  "companyName": "<company name>",
  "requirement": "<detailed requirements>",
  "salary": "<salary range>",
  "location": "<work location>",
  "jobType": "<employment type>",
  "education": "<education requirement>",
  "experience": "<experience requirement>",
  "status": "ACTIVE"
}
EOF
```

#### Step 4: Confirm Success

After successful publication, inform the user and **save the returned job ID** for future operations (update, delete, list matches). The token is automatically saved.

---

### Update Job (action: update)

Requires the **jobId** from a previous publish. Only changed fields need to be provided. The script will automatically use the saved token.

```bash
cat <<EOF | python3 scripts/publish_job.py
{
  "action": "update",
  "jobId": "<job id>",
  "salary": "<new salary range>",
  "requirement": "<updated requirements>"
}
EOF
```

Updatable fields: `title`, `companyName`, `requirement`, `salary`, `location`, `jobType`, `education`, `experience`, `status`.

---

### Delete Job (action: delete)

Soft-deletes the job posting by marking it as INACTIVE. Match history is preserved.

```bash
cat <<EOF | python3 scripts/publish_job.py
{
  "action": "delete",
  "jobId": "<job id>"
}
EOF
```

---

### View Jobs and Matches (get_profile.py)

Check your published jobs and matched candidates without making any changes.

#### View All Jobs

```bash
cat <<EOF | python3 scripts/get_profile.py
{
  "action": "jobs"
}
EOF
```

#### View Specific Job Details

```bash
cat <<EOF | python3 scripts/get_profile.py
{
  "action": "job",
  "jobId": "<job id>"
}
EOF
```

#### View Matches for Specific Job

```bash
cat <<EOF | python3 scripts/get_profile.py
{
  "action": "matches",
  "jobId": "<job id>"
}
EOF
```

#### View All Matches Across All Jobs

```bash
cat <<EOF | python3 scripts/get_profile.py
{
  "action": "all-matches"
}
EOF
```

#### View Full Information (all jobs + all matches)

```bash
cat <<EOF | python3 scripts/get_profile.py
{
  "action": "full"
}
EOF
```

**When to use get_profile.py:**
- User asks "What jobs have I published?" or "Show me my jobs"
- User wants to check matches across all jobs
- User wants to review job details before updating
- User asks "Do I have any candidates?"

---

### List Matched Candidates (action: matches)

Retrieve candidates matched by the AI system for a specific job posting and provide comprehensive multi-dimensional analysis.

```bash
cat <<EOF | python3 scripts/publish_job.py
{
  "action": "matches",
  "jobId": "<job id>"
}
EOF
```

#### Step 1: Retrieve Matched Candidates

The API returns a list of matched candidates with similarity scores. Each match includes:
- Candidate details (name, resume, skills, experience, etc.)
- Similarity score (0-1 range, based on vector matching)
- Match metadata

#### Step 2: Generate Multi-Dimensional Analysis

After retrieving the matches, Claude MUST provide a comprehensive analysis for EACH matched candidate. The analysis should cover:

**1. Overall Match Assessment (总体匹配评估)**
- Match score interpretation (优秀/良好/中等/一般)
- Quick summary of why this candidate matches or doesn't match

**2. Skill Alignment Analysis (技能匹配分析)**
- ✅ Matching skills: List candidate skills that align with job requirements
- ⚠️ Skill gaps: Identify required skills the candidate lacks
- 💡 Bonus skills: Highlight additional valuable skills the candidate brings
- Skill match percentage estimate (e.g., "90% skill match")

**3. Experience Fit Analysis (经验匹配分析)**
- Years of experience comparison (required vs. actual)
- Industry/domain experience relevance
- Project complexity and scale alignment
- Seniority level match (junior/mid/senior)
- Career progression trajectory

**4. Education & Qualifications (学历与资质)**
- Education level match
- Relevant certifications
- Academic background relevance

**5. Cultural & Team Fit (文化与团队契合度)**
- Work style indicators from resume
- Team collaboration experience
- Leadership potential (if applicable)
- Communication skills evidence

**6. Compensation Expectations (薪资期望)**
- Candidate's salary expectations vs. job offer
- Negotiation room assessment
- Total compensation considerations

**7. Advantages & Disadvantages (优劣势分析)**

**Advantages (优势):**
- List 3-5 key strengths of this candidate
- Why this candidate stands out
- Unique value propositions

**Disadvantages (劣势):**
- List 2-4 potential concerns or gaps
- Risk factors to consider
- Areas where the candidate might need support

**8. Hiring Recommendation (招聘建议)**
- Priority level: 🔥 High Priority / ⭐ Medium Priority / 💭 Consider
- Recommended action: "Strongly recommend interview" / "Worth considering" / "Proceed with caution"
- Suggested interview focus areas
- Onboarding considerations

**9. Interview Strategy (面试策略)**
- Key areas to probe during interview
- Technical assessment recommendations
- Behavioral questions to ask
- Red flags to watch for

**10. Retention & Growth Potential (留任与成长潜力)**
- Long-term fit assessment
- Growth trajectory within the company
- Retention risk factors
- Development opportunities needed

#### Step 3: Provide Comparative Summary

After analyzing individual candidates, provide a comparative summary:

**Top 3 Recommendations:**
Rank the top 3 candidates with brief rationale for each.

**Candidate Distribution:**
- Excellent matches (score > 0.85): X candidates
- Good matches (score 0.75-0.85): Y candidates
- Moderate matches (score 0.65-0.75): Z candidates

**Hiring Strategy Advice:**
- Which candidates to prioritize for interviews
- Suggested interview panel composition
- Timeline recommendations
- Backup candidate strategy

#### Output Format Example

```
📊 候选人匹配分析报告
职位: 高级 Python 后端工程师 @ 拼多多

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 候选人 #1: 张伟
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 总体匹配度: 0.89 (优秀匹配)
这是一位高度匹配的候选人，技能和经验都非常符合岗位要求。

🔧 技能匹配分析 (90% 匹配)
✅ 匹配技能:
  • Python (4年实战经验) - 完全匹配
  • Django/Flask 框架 - 完全匹配
  • MySQL, Redis 数据库 - 完全匹配
  • RESTful API 设计 - 完全匹配
  • 电商系统经验 - 完全匹配 (加分项)

💡 额外技能 (超出要求):
  • Docker 容器化部署
  • 支付系统集成经验
  • 高并发优化经验

⚠️ 技能缺口:
  • Kubernetes (岗位优先，候选人未提及)
  • 微服务架构 (提及较少)

💼 经验匹配分析
• 要求: 3-5年 | 候选人: 4年 ✅ 完全匹配
• 行业经验: 电商支付、订单系统 - 与拼多多业务高度相关
• 项目规模: 处理过高并发场景，符合大厂要求
• 职级匹配: 高级工程师水平，符合岗位定位

🎓 学历与资质
• 学历: 本科 ✅ 符合要求
• 专业: 计算机相关专业
• 证书: [简历中未提及]

🤝 文化与团队契合度
• 团队协作: 简历中体现跨部门协作经验
• 沟通能力: 项目描述清晰，表达能力强
• 主动性: 主导过系统优化项目，显示主动性

💰 薪资期望
• 候选人期望: 30k-45k
• 岗位提供: 25k-40k
• 评估: 期望略高于上限，但在可协商范围内
• 建议: 可以 38k-40k 作为起点进行谈判

✅ 优势分析
1. 技能栈高度匹配，可以快速上手
2. 电商行业经验丰富，业务理解深入
3. 有高并发系统优化经验，符合拼多多需求
4. 支付系统经验是稀缺加分项
5. 工作年限适中，性价比高

⚠️ 劣势分析
1. 缺少 K8s 经验，可能需要培训
2. 微服务架构经验不足，需要评估
3. 薪资期望略高，需要协商
4. 简历中未体现大厂背景 (如果看重的话)

🎯 招聘建议
优先级: 🔥 强烈推荐面试

建议行动:
• 立即安排初筛电话面试
• 重点评估系统设计能力和高并发处理经验
• 准备技术面试，侧重 Python 高级特性和数据库优化
• HR 提前沟通薪资预期，评估协商空间

📝 面试策略
技术面试重点:
• Python 高级特性 (装饰器、异步编程、性能优化)
• 数据库设计与优化 (索引、查询优化、分库分表)
• 系统设计能力 (高并发架构、缓存策略)
• 电商业务理解 (支付流程、订单系统)

建议面试问题:
• 描述一下你处理过的最高并发场景，如何优化的?
• 支付系统中如何保证数据一致性?
• 如果让你设计拼多多的订单系统，你会如何设计?
• 你对微服务架构有什么理解? (评估学习能力)

需要关注的红旗:
• 对 K8s 和微服务的态度 (是否愿意学习)
• 薪资谈判的灵活度
• 对加班和工作强度的接受度

🚀 留任与成长潜力 (⭐⭐⭐⭐)
• 长期契合度: 高 - 技能和业务匹配度高
• 成长空间: 可以从高级工程师成长为技术专家
• 留任风险: 中等 - 薪资期望需要满足
• 发展建议: 提供微服务和云原生技术的学习机会

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[继续分析其他候选人...]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 综合对比与招聘建议
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🏆 Top 3 推荐候选人:

1. 🥇 张伟 (0.89)
   理由: 技能高度匹配，电商经验丰富，可快速上手

2. 🥈 李明 (0.85)
   理由: 大厂背景，技术全面，但薪资要求较高

3. 🥉 王芳 (0.81)
   理由: 学习能力强，潜力大，性价比高

📈 候选人分布:
• 优秀匹配 (>0.85): 3 位候选人
• 良好匹配 (0.75-0.85): 5 位候选人
• 中等匹配 (0.65-0.75): 2 位候选人

💡 招聘策略建议:

1. **面试优先级**
   • 第一批: 张伟、李明 (本周内安排)
   • 第二批: 王芳、赵强 (下周安排)
   • 备选: 其他良好匹配候选人

2. **面试团队配置**
   • 技术面试: 技术总监 + 高级工程师
   • HR 面试: 评估文化契合度和薪资协商
   • 终面: 部门负责人

3. **时间规划**
   • 目标: 2周内完成前 5 位候选人面试
   • 预留 1 周进行 offer 谈判
   • 预计 3-4 周内完成招聘

4. **备选方案**
   • 如果前 3 位都未通过，立即启动第二批
   • 考虑适当放宽 K8s 经验要求，入职后培训
   • 薪资预算可以适当上调 5k 以吸引优质候选人

5. **风险提示**
   • 优秀候选人可能同时面试多家公司，需要加快流程
   • 薪资期望普遍略高于预算，需要 HR 提前准备谈判策略
   • 建议准备 2-3 个 backup 候选人

🎯 后续行动清单:
□ HR 联系前 3 位候选人，安排初筛
□ 准备技术面试题库和评分标准
□ 与财务确认薪资调整空间
□ 准备 offer 模板和入职流程
□ 设置面试反馈收集机制

```

#### Important Notes

- **Always provide detailed analysis**: Don't just list candidates with scores. Hiring managers need actionable insights.
- **Be objective about gaps**: Help identify areas where candidates might need support or training.
- **Consider total value**: Match score is just one factor; potential, cultural fit, and long-term growth matter too.
- **Prioritize actionability**: Every analysis should lead to clear hiring decisions and interview strategies.
- **Personalize recommendations**: Reference specific details from the job requirements in your analysis.
- **Think long-term**: Consider not just immediate fit, but retention and growth potential.

---

## API Configuration

Default API endpoint: `https://api.jobclaw.ai`

To use a different endpoint, modify the `apiUrl` parameter when calling the script.

## Error Handling

If any operation fails:

- Check if the API server is running
- Verify all required fields are provided
- Ensure the API endpoint is correct
- For update/delete/matches: ensure a valid **jobId** is provided
- Review the error message and guide the user accordingly

## Resources

### scripts/publish_job.py

Python script supporting four actions (`publish`, `update`, `delete`, `matches`):

- Creating new recruiter accounts (auto-created on publish)
- Publishing and updating job postings
- Soft-deleting job postings (mark INACTIVE)
- Listing AI-matched candidates

The script uses Python's built-in `urllib` library (no external dependencies required).
