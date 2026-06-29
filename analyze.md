# EC Website Rebuild — WBS, Requirements & Estimation

> Phạm vi: Làm mới website EC trên nền **WordPress**, kiến trúc **đa ngôn ngữ-ready**
> nhưng **go-live tiếng Anh trước**. Tích hợp **WooCommerce** (catalog) +
> **Paddle overlay checkout (MoR — tax/VAT)** + **Keygen.sh (license management)**.
> Các ngôn ngữ ngoài tiếng Anh được **tách thành phase riêng (Phase L)** và **báo giá theo từng ngôn ngữ**.
> Đơn vị estimation: **MD = man-day**.

---

## 1. Yêu cầu chức năng (Functional Requirements)

| ID | Nhóm | Yêu cầu |
|----|------|---------|
| FR-01 | Đa ngôn ngữ | Kiến trúc đa ngôn ngữ-ready; **EN active trước**, thêm ngôn ngữ mới chỉ qua cấu hình + nhập nội dung |
| FR-02 | Đa ngôn ngữ | Language switcher; URL theo locale (`/en`, `/ja`…); hreflang đầy đủ |
| FR-03 | Điều hướng | Mega menu (Products/Services/Learn/Communities/Support) + footer nhiều cột |
| FR-04 | Trang chủ | Hero, khối "500+ titles", nizima/JUKU, community, education cards, news feed |
| FR-05 | Sản phẩm | Trang Cubism Editor/SDK; bảng so sánh FREE/PRO; bảng spec |
| FR-06 | Download | Tải SDK đa nền tảng (Unity/Web/Native/Java/Unreal/Cocos); trial 42 ngày; changelog |
| FR-07 | Tin tức | Listing theo ngày + filter category (Sale/News/Update/Event/Awards) + trang chi tiết |
| FR-08 | Học liệu/Cộng đồng | Manual/tutorial links; Communities directory; Discord/Chapters |
| FR-09 | Forms | Contact/Help; đăng ký Student, LEAP/Edu, Creative Awards |
| FR-10 | Thương mại | WooCommerce catalog; product ↔ Paddle Price ID; giỏ hàng |
| FR-11 | Thanh toán | Paddle overlay checkout; Paddle là MoR xử lý thuế/VAT/hóa đơn |
| FR-12 | Thanh toán | Localized pricing theo vùng; subscription (nếu PRO theo kỳ) |
| FR-13 | Đơn hàng | Đồng bộ order Woo ↔ Paddle; webhook xác thực chữ ký + idempotency |
| FR-14 | License | Tạo license Keygen theo policy (PRO/Trial/Student/Edu/Awards) khi thanh toán xong |
| FR-15 | License | Refund/chargeback → suspend/revoke; trial hết hạn → tự khóa |
| FR-16 | License | My Account: xem key, machines, activate/deactivate, tải hóa đơn |
| FR-17 | License | Cubism Editor activate/validate qua Keygen API (node-locked/floating) |
| FR-18 | Vận hành | Phân quyền editor cho team nội dung tự cập nhật news/sale/sản phẩm |

## 2. Yêu cầu phi chức năng (Non-Functional Requirements)

| ID | Nhóm | Yêu cầu |
|----|------|---------|
| NFR-01 | SEO | Multilingual-ready SEO, hreflang/canonical, sitemap, schema; giữ ranking qua 301 redirect |
| NFR-02 | Performance | LCP < 2.5s; caching + CDN; tối ưu ảnh/video hero; lazy-load |
| NFR-03 | Security | Hardening WP, xác thực chữ ký webhook, không lộ Keygen/Paddle secret, rate limit |
| NFR-04 | Compliance | GDPR/cookie consent; thuế do Paddle (MoR) đảm trách, không tính trùng ở Woo |
| NFR-05 | Reliability | Webhook idempotent + retry; đối soát Woo↔Paddle↔Keygen khớp |
| NFR-06 | Accessibility | WCAG 2.1 AA cơ bản |
| NFR-07 | Compatibility | Responsive desktop/tablet/mobile; trình duyệt hiện đại |
| NFR-08 | Maintainability | Reusable blocks/patterns; **string externalization** (không hardcode chữ); tài liệu vận hành; staging + CI/CD |
| NFR-09 | Backup/DR | Backup tự động + phương án rollback go-live |
| NFR-10 | Analytics | GA4 + event tracking (download, checkout, license activate) |
| NFR-11 | i18n-ready | Mọi template/chuỗi/format (ngày, số, tiền) tách khỏi code; thêm ngôn ngữ mới không cần sửa code |

---

## 3. Nguyên tắc kiến trúc đa ngôn ngữ (để thêm ngôn ngữ "dễ")

Mục tiêu: thêm 1 ngôn ngữ mới = **cấu hình + nhập bản dịch**, KHÔNG đụng code/template.

- **WPML + WooCommerce Multilingual** (hoặc Polylang Pro) — cài & cấu trúc ngay từ đầu dù chỉ bật EN.
- **String externalization**: 100% chữ trong theme nằm trong `.pot/.po` (gettext) hoặc String Translation, không hardcode.
- **Cấu trúc URL theo locale** + hreflang scaffold sẵn 7 slot ngôn ngữ.
- **Template trung lập layout**: thiết kế chừa **text expansion** (DE/EN dài hơn), hỗ trợ **CJK/Thai font** & dấu tiếng Việt/ES.
- **Tách format vùng**: ngày/giờ/số/tiền render theo locale (không cứng định dạng).
- **Quy trình dịch chuẩn hóa**: glossary + memory + export/import; nội dung mới tạo ở EN → workflow dịch.
- **Paddle localized pricing**: bật theo vùng, không phụ thuộc ngôn ngữ UI.

→ Nhờ đó **Phase L** mỗi ngôn ngữ chỉ tốn chi phí cấu hình + nhập nội dung + QA, không phát triển lại.

---

## 4. Work Breakdown Structure + Estimation (MD)

### Phase 0 — Discovery, UX/UI Design

| Task | MD |
|------|----|
| Requirement workshop & BA (chốt FR/NFR) | 5 |
| Audit & content inventory site EN hiện tại | 3 |
| IA & sitemap design | 3 |
| Technical architecture & integration spec (Paddle/Keygen) | 5 |
| **Thiết kế i18n strategy** (string, locale routing, workflow dịch) | 3 |
| UX wireframes (các template chính, chừa text expansion) | 8 |
| UI visual design (hero, product, news, checkout, account) | 12 |
| Design system / component library | 5 |
| **Subtotal** | **44** |

### Phase 1 — Nền tảng (EN-first, multilingual-ready)

| Task | MD |
|------|----|
| WordPress base + theme scaffolding | 5 |
| WPML + WooCommerce Multilingual setup (ready, chỉ bật EN) | 4 |
| i18n implementation: string externalization + locale routing + hreflang scaffold | 4 |
| Migration nội dung **EN** từ site cũ | 5 |
| 301 redirect mapping (EN) | 2 |
| **Subtotal** | **20** |

### Phase 2 — Theme & Templates (build nội dung — EN)

| Task | MD |
|------|----|
| Header mega menu + footer | 5 |
| Homepage blocks | 10 |
| Reusable Gutenberg blocks/patterns | 8 |
| Product detail + bảng so sánh FREE/PRO | 5 |
| Downloads + SDK đa nền tảng + changelog (CPT) | 6 |
| News/Event listing + filter category + detail | 5 |
| Learn/Community/Communities directory | 4 |
| Trang tĩnh/pháp lý (license, company, careers) | 3 |
| Forms (Contact/Student/LEAP/Awards) | 5 |
| Responsive + cross-browser polish | 6 |
| **Subtotal** | **57** |

### Phase 3 — WooCommerce + Paddle (MoR)

| Task | MD |
|------|----|
| WooCommerce setup + mô hình catalog | 5 |
| Product ↔ Paddle Price ID mapping | 3 |
| Tích hợp Paddle.js overlay checkout | 6 |
| Webhook handler (verify signature + idempotency) | 6 |
| Đồng bộ order Woo ↔ Paddle | 5 |
| Tắt tax Woo / cấu hình MoR Paddle | 2 |
| Localized pricing theo vùng | 3 |
| Subscription (nếu PRO theo kỳ) | 5 |
| Refund/chargeback flow | 4 |
| **Subtotal** | **39** |

### Phase 4 — Keygen.sh (License Management)

| Task | MD |
|------|----|
| Định nghĩa policies (PRO/Trial/Student/Edu/Awards) | 3 |
| Tạo license qua webhook | 5 |
| Suspend/revoke khi refund + trial expiry | 4 |
| My Account license dashboard | 8 |
| Email license + link hóa đơn | 3 |
| Verify activate/validate phía Cubism Editor | 4 |
| **Subtotal** | **27** |

### Phase 5 — NFR / Cross-cutting

| Task | MD |
|------|----|
| SEO (multilingual-ready) + schema + sitemap | 5 |
| Performance (cache/CDN/optim media) | 5 |
| Security hardening + GDPR/cookie consent | 4 |
| Analytics GA4 + events | 3 |
| Accessibility WCAG AA cơ bản | 4 |
| Backup + staging + CI/CD | 4 |
| Role/permission setup | 2 |
| **Subtotal** | **27** |

### Phase 6 — QA, UAT & Launch (EN)

| Task | MD |
|------|----|
| Test plan + test cases | 4 |
| Functional QA (EN) | 6 |
| E2E payment + license (sandbox Paddle/Keygen) | 8 |
| UAT support + fixes | 8 |
| Migration dry-run + go-live | 5 |
| Post-launch hypercare | 5 |
| **Subtotal** | **36** |

### Quản trị dự án (xuyên suốt — giai đoạn EN)

| Task | MD |
|------|----|
| PM / coordination / reporting | 14 |
| **Subtotal** | **14** |

---

## 5. Phase L — Localization (mỗi ngôn ngữ ngoài EN — báo giá riêng)

Điều kiện: nền tảng đã i18n-ready (Phase 1). **Chi phí dưới đây là kỹ thuật + tích hợp + QA**,
giả định **bản dịch nội dung do khách/vendor cung cấp** (xem ghi chú về dịch thuật bên dưới).

**Chi phí cho MỖI ngôn ngữ thêm:**

| Task | MD |
|------|----|
| Thêm ngôn ngữ + cấu hình locale URL + hreflang | 0.5 |
| Import bản dịch UI/theme + WooCommerce strings | 1.5 |
| Nhập nội dung (pages/products/news/legal) vào WPML | 3.0 |
| Localized pricing (Paddle region) + currency | 0.5 |
| Điều chỉnh typography/layout (CJK/Thai, text expansion) | 1.0 |
| QA + proofreading pass | 1.5 |
| **Đơn giá / 1 ngôn ngữ** | **8 MD** |

**Báo giá theo 6 ngôn ngữ còn lại:**

| Ngôn ngữ | MD |
|----------|----|
| 日本語 (JA) | 8 |
| 中文 (ZH) | 8 |
| 한국어 (KO) | 8 |
| ไทย (TH) | 8 |
| Español (ES) | 8 |
| Indonesia (ID) | 8 |
| **Tổng 6 ngôn ngữ** | **48** |

> **Ghi chú dịch thuật:** 8 MD/ngôn ngữ **không bao gồm chi phí dịch nội dung (copywriting)**.
> - Nếu khách cung cấp bản dịch sẵn → giữ nguyên 8 MD/ngôn ngữ.
> - Nếu cần team dịch (in-house) → **+2–4 MD/ngôn ngữ** tùy khối lượng từ.
> - Nếu thuê vendor dịch → tính riêng theo **đơn giá/từ** (không tính vào MD dev).
> - CJK/Thai có thể phát sinh thêm font/layout → đã dự phòng trong 1.0 MD typography.

---

## 6. Tổng hợp Estimation

### Giai đoạn EN (go-live tiếng Anh)

| Phase | MD |
|-------|----|
| 0 — Discovery & Design | 44 |
| 1 — Foundation (EN, i18n-ready) | 20 |
| 2 — Theme & Templates | 57 |
| 3 — WooCommerce + Paddle | 39 |
| 4 — Keygen Licensing | 27 |
| 5 — NFR / Cross-cutting | 27 |
| 6 — QA & Launch | 36 |
| PM | 14 |
| **Tổng EN (chưa contingency)** | **264** |
| Contingency ~15% | ~40 |
| **Tổng EN (đề xuất)** | **~304 MD** |

### Localization (tùy chọn, cộng thêm)

| Hạng mục | MD |
|----------|----|
| Mỗi ngôn ngữ thêm | 8 |
| Cả 6 ngôn ngữ | 48 (+ contingency ~7 → ~55) |

**Tổng nếu làm full 7 ngôn ngữ:** ~304 + ~55 ≈ **~359 MD**

---

## 7. Roadmap thực thi

Team **~5 người** (1 PM/BA, 1 Designer, 2 WP/FE-BE dev, 1 QA; DevOps part-time).

### Track 1 — Go-live EN (~304 MD → ~13–15 tuần)

```
Tuần:   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15
P0   [#######]                                                      Discovery + Design
P1       [######]                                                   Foundation EN (i18n-ready)
P2          [###################]                                   Theme & Templates
P3                      [############]                              WooCommerce + Paddle
P4                           [##########]                           Keygen Licensing
P5                                [##########]                      NFR / Cross-cutting
P6                                        [##############]          QA / UAT / Launch EN
PM   [==============================================================] xuyên suốt
```

**Milestones EN:**
- **M1 (T3):** Chốt design + spec tích hợp + i18n strategy.
- **M2 (T5):** Nền tảng EN + i18n-ready chạy.
- **M3 (T8):** Template/nội dung EN dựng xong trên staging.
- **M4 (T11):** Luồng mua → Paddle → Keygen chạy thông trên sandbox.
- **M5 (T13):** Hoàn tất NFR (SEO/perf/security).
- **M6 (T15):** UAT pass → **go-live EN** + hypercare.

### Track 2 — Localization (sau khi EN ổn định)

```
Tuần:  16  17  18  19  20  21  22
       [JA/ZH] [KO/TH] [ES/ID]
```
- Chạy theo cặp ngôn ngữ, mỗi cặp ~2 tuần (2 dev song song); ~6 tuần cho 6 ngôn ngữ.
- Có thể bắt đầu sớm hơn (overlap với Phase 6) nếu nền i18n đã nghiệm thu ở M2 và có sẵn bản dịch.

---

## 8. Giả định & Rủi ro

**Giả định**
- Đã có tài khoản Paddle (MoR active) và Keygen.sh.
- Cubism Editor đã/đang tích hợp Keygen (chỉ cần verify, không build lại client).
- Dùng theme tùy biến trên Gutenberg (không phải page builder nặng).
- Bản dịch nội dung (Phase L) do khách/vendor cung cấp, trừ khi chọn option dịch in-house.

**Rủi ro chính**
- **i18n-ready phải làm đúng từ đầu** — nếu hardcode chữ ở Phase 2, chi phí thêm ngôn ngữ sẽ đội lên nhiều.
- **Migration EN**: redirect/hreflang sai → mất SEO.
- **Đối soát doanh thu**: Paddle là MoR nên hóa đơn/thuế nằm ở Paddle, Woo chỉ là bản ghi nội bộ.
- **Idempotency webhook**: tránh tạo trùng license khi Paddle retry.
- Chất lượng/khối lượng bản dịch có thể phát sinh thêm MD (đã có option/ghi chú ở Phase L).
