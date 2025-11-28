## ⚠️ **Required:** Replace all placeholders marked with `[REPLACE_ME: ...]` before creating this PR.

## ⚠️ **Additionally**: For any checklist section, select the appropriate option by changing the corresponding [ ] to [x] and leave the others unchecked. You can check these with a click after the PR has been created also.

---

# 📰 **Changes**

## 🛠️ **Implementation Details**

[REPLACE_ME: Describe the specific modifications introduced in this change]

---

# 📘 **Post-Implementation Validation (If Needed)**

## 🗓️ **Validation Details**

**• Validation Date:**
[REPLACE_ME: DD/MM/YYYY]

**• Validation Performed By:**
[REPLACE_ME: Full Name]

**• Security Testing Performed:**

- [ ] Yes
- [ ] No
- [ ] N/A
- [ ] Manual Testing

## 📝 **Validation Notes**

[REPLACE_ME: Summarize findings and confirm whether the change has no adverse security effects]

---

# 🔒 **Security Review Checklist**

Use this checklist to confirm that key security considerations were reviewed and validated after implementation.

---

## 1️⃣ **Input Validation**

- Ensure all input is validated, sanitized, and escaped.
- Prefer whitelisting over blacklisting.
- Validate data size, type, and range.

- [ ] Done

---

## 2️⃣ **Authentication & Authorization**

- Implement strong passwords and multi-factor authentication (MFA).
- Use role-based access control (RBAC) and enforce least privilege.
- Never hardcode credentials or secrets.

- [ ] Done

---

## 3️⃣ **Secure Data Handling**

- Encrypt sensitive data at rest and in transit (AES-256, TLS 1.2/1.3).
- Avoid logging sensitive data.
- Use secure database access (e.g., parameterized queries, ORM).

- [ ] Done

---

## 4️⃣ **Error & Exception Handling**

- Do not expose detailed errors to end users.
- Log technical details securely.
- Sanitize any data included in error responses.

- [ ] Done

---

## 5️⃣ **Session Management**

- Use secure, HttpOnly cookies with `Secure` and `SameSite` flags.
- Enforce session timeouts and logout invalidation.
- Ensure session IDs are unique and unpredictable.

- [ ] Done

---

## 6️⃣ **Dependencies & Libraries**

- Regularly update and patch third-party dependencies.
- Use vulnerability scanning tools (e.g., OWASP Dependency-Check).
- Verify integrity and authenticity of open-source components.

- [ ] Done

---

## 7️⃣ **Secure API Design**

- Use HTTPS and secure authentication mechanisms (OAuth 2.0).
- Validate API requests and responses.
- Limit API exposure and apply rate-limiting.

- [ ] Done

---

## 8️⃣ **Output Encoding & Escaping**

- Encode and escape output to prevent injection attacks such as XSS.
- Use context-specific escaping for HTML, JavaScript, and SQL.

- [ ] Done

---

## 9️⃣ **Logging & Monitoring**

- Log security events while excluding sensitive data.
- Monitor logs for suspicious patterns.
- Use SIEM or centralized monitoring tools where available.

- [ ] Done

---

## 🔟 **Secure Build & Deployment**

- Perform static and dynamic analysis as part of CI/CD.
- Remove unused code, debug information,

- [ ] Done
