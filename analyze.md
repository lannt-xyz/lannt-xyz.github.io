# EC Website Rebuild — WBS, Requirements & Estimation

> Phạm vi: Làm mới website EC trên nền **WordPress**, kiến trúc **đa ngôn ngữ-ready**
> nhưng **go-live tiếng Anh trước**. Tích hợp **WooCommerce** (catalog) +
> **Paddle overlay checkout (MoR — tax/VAT)** + **Reprise RLM Cloud (license management)**.
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
| FR-10 | Thương mại | WooCommerce: **1 product Cubism PRO**, variant = tier (Indie/Business/Student) × plan (Monthly/Annual/3-Year) ↔ Paddle Price ID; **single-item checkout**; seat = quantity (khớp store hiện hành) |
| FR-11 | Thanh toán | Paddle overlay checkout; Paddle là MoR xử lý thuế/VAT/hóa đơn |
| FR-12 | Thanh toán | Localized pricing theo vùng; subscription (nếu PRO theo kỳ) |
| FR-13 | Đơn hàng | Đồng bộ order Woo ↔ Paddle; webhook xác thực chữ ký + idempotency |
| FR-14 | License | Tạo license RLM Cloud theo policy (PRO/**Trial**/Student/Edu/Awards) khi mua xong; **Try → cấp trial license** |
| FR-15 | License | Refund/chargeback → suspend/revoke; trial hết hạn → tự khóa |
| FR-16 | License | My Account: xem/tra license key, deactivate/chuyển máy (max 2 PC/license), order history, quản lý subscription, coupon student — **[ĐIỀU TRA] đã tồn tại trên store hiện hành, làm theo cái có** |
| FR-17 | License | Cubism Editor activate/validate qua **Reprise RLM Cloud** (cloud activation) |
| FR-18 | Vận hành | Phân quyền editor cho team nội dung tự cập nhật news/sale/sản phẩm |
| FR-19 | Tiện ích | Site search (tìm kiếm toàn site) |
| FR-20 | Tài khoản | Account/Auth: đăng ký/đăng nhập/reset mật khẩu (tiền đề My Account) |
| FR-21 | Services/Learn | nizima/JUKU/Creative Studio và manual/tutorial là **outbound link** (giữ như hiện hành); chỉ Sample Data nội bộ |

## 2. Yêu cầu phi chức năng (Non-Functional Requirements)

| ID | Nhóm | Yêu cầu |
|----|------|---------|
| NFR-01 | SEO | Multilingual-ready SEO, hreflang/canonical, sitemap, schema; giữ ranking qua 301 redirect |
| NFR-02 | Performance | LCP < 2.5s; caching + CDN; tối ưu ảnh/video hero; lazy-load |
| NFR-03 | Security | Hardening WP, xác thực chữ ký webhook, không lộ RLM Cloud/Paddle secret, rate limit |
| NFR-04 | Compliance | GDPR/cookie consent; thuế do Paddle (MoR) đảm trách, không tính trùng ở Woo |
| NFR-05 | Reliability | Webhook idempotent + retry; đối soát Woo↔Paddle↔RLM Cloud khớp |
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
| Technical architecture & integration spec (Paddle/RLM Cloud) | 5 |
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
| Communities directory + Sample Data (nội bộ); Services/Learn chỉ outbound link | 3 |
| Trang tĩnh/pháp lý (license, company, careers) | 3 |
| Forms (Contact/Student/LEAP/Awards) | 5 |
| Site search (FR-19) | 2 |
| Responsive + cross-browser polish | 6 |
| **Subtotal** | **58** |

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

### Phase 4 — Reprise RLM Cloud (License Management)

| Task | MD |
|------|----|
| Định nghĩa policies (PRO/Trial/Student/Edu/Awards) | 3 |
| Tạo license qua webhook (gồm trial license khi "Try") | 5 |
| Suspend/revoke khi refund + trial expiry | 4 |
| Account/Auth (đăng ký/đăng nhập/reset — FR-20) | 2 |
| My Account license dashboard | 8 |
| Email license + link hóa đơn | 3 |
| Tích hợp **Reprise RLM Cloud** activation cho Cubism Editor (FR-17) | 4 |
| **Subtotal** | **29** |

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
| E2E payment + license (sandbox Paddle/RLM Cloud) | 8 |
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

## 5b. Phase M — Data Migration: Welcart → WooCommerce (báo giá riêng, ĐÃ XÁC NHẬN in-scope)

**[USER xác nhận]** Store hiện hành chạy **Welcart**, yêu cầu **migrate sang WooCommerce**. Tách báo giá riêng theo yêu cầu, nhưng là hạng mục **bắt buộc** (không phải tùy chọn).

> ⚠️ Migration **khác plugin** (Welcart → WooCommerce), schema riêng → nặng hơn migration cùng nền; rủi ro cao nhất ở subscription đang active.

| Task | MD |
|------|----|
| Reverse-engineer schema Welcart (customer/order/subscription/license) | 4 |
| Mapping Welcart → WooCommerce data model | 3 |
| Migration tài khoản khách (export/import + flow reset mật khẩu) | 4 |
| Migration lịch sử đơn hàng/subscription đang chạy | 5 |
| Đối soát & map license cũ → RLM Cloud | 5 |
| Validate dữ liệu + dry-run + cutover | 3 |
| **Subtotal** | **24** |
| Contingency ~20% (migration khác plugin, rủi ro cao) | ~5 |
| **Tổng Migration (đề xuất)** | **~29 MD** |

> Phụ thuộc lớn vào chất lượng/định dạng DB Welcart và **subscription đang active** (phải chuyển sang Paddle không gián đoạn billing) — cần khảo sát thực tế DB ở bước spec, có thể phát sinh thêm.

### 5b.1 — 3 điểm rủi ro then chốt của migration (BẮT BUỘC khảo sát sớm)

Ba điểm dưới đây quyết định **độ khả thi** và có thể **đẩy MD lên** nếu chủ quan. Phải đưa vào **technical discovery** ngay đầu dự án.

**① Khác plugin hoàn toàn (Welcart `usces_*` → WooCommerce)**
- Data model Welcart khác Woo; **không có công cụ chuyển thẳng** → phải reverse-engineer + viết script mapping riêng.
- Rủi ro: mất/sai dữ liệu khách, đơn, coupon, thuế lịch sử nếu mapping thiếu.
- Cần lấy: full schema + dump DB Welcart (bảng customer/order/subscription/coupon/license).

**② Subscription đang active — ĐIỂM KHÓ NHẤT**
- Khách đang trả theo kỳ trên Welcart (credit card/PayPal) phải chuyển sang **Paddle** mà **KHÔNG gián đoạn billing** và **KHÔNG bắt khách nhập lại thẻ**.
- Token thẻ ở cổng thanh toán cũ thường **không port được** sang Paddle → cần chiến lược: re-subscribe có hướng dẫn, song song 2 hệ trong giai đoạn chuyển tiếp, hoặc thỏa thuận với Paddle về import.
- Rủi ro: mất doanh thu định kỳ, churn khách nếu xử lý sai.
- Cần lấy: cơ chế thanh toán/subscription hiện tại, chu kỳ gia hạn, số sub đang active, hợp đồng cổng cũ.

**③ License đang hoạt động (max 2 PC/license) → RLM Cloud**
- Phải map license + **trạng thái activation hiện tại** sang RLM Cloud, giữ nguyên để khách **không bị khóa** phần mềm.
- Rủi ro: khách đang dùng bị deactivate đột ngột, hoặc activation count sai.
- Cần lấy: danh sách license + máy đã activate, mô hình activation hiện hành, khả năng import của RLM Cloud.

> **Khuyến nghị:** chạy **technical discovery cho migration** TRƯỚC khi chốt giá Phase M — nếu ②/③ phức tạp hơn dự kiến, MD và rủi ro sẽ tăng đáng kể.

---

## 6. Tổng hợp Estimation

### Giai đoạn EN (go-live tiếng Anh)

| Phase | MD |
|-------|----|
| 0 — Discovery & Design | 44 |
| 1 — Foundation (EN, i18n-ready) | 20 |
| 2 — Theme & Templates | 58 |
| 3 — WooCommerce + Paddle | 39 |
| 4 — Licensing + Account | 29 |
| 5 — NFR / Cross-cutting | 27 |
| 6 — QA & Launch | 36 |
| PM | 14 |
| **Tổng EN (chưa contingency)** | **267** |
| Contingency ~15% | ~40 |
| **Tổng EN (đề xuất)** | **~307 MD** |

### Hạng mục báo giá riêng (cộng thêm)

| Hạng mục | MD | Trạng thái |
|----------|----|-----------|
| Data migration (Phase M — Welcart→Woo) | ~29 | **bắt buộc** (đã xác nhận) |
| Mỗi ngôn ngữ thêm (Phase L) | 8 | tùy chọn |
| Cả 6 ngôn ngữ | 48 (+ contingency ~7 → ~55) | tùy chọn |

**Tối thiểu (EN + migration bắt buộc):** ~307 + ~29 ≈ **~336 MD**
**Full (7 ngôn ngữ + migration):** ~307 + ~55 + ~29 ≈ **~391 MD**

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
P4                           [##########]                           RLM Cloud Licensing
P5                                [##########]                      NFR / Cross-cutting
P6                                        [##############]          QA / UAT / Launch EN
PM   [==============================================================] xuyên suốt
```

**Milestones EN:**
- **M1 (T3):** Chốt design + spec tích hợp + i18n strategy.
- **M2 (T5):** Nền tảng EN + i18n-ready chạy.
- **M3 (T8):** Template/nội dung EN dựng xong trên staging.
- **M4 (T11):** Luồng mua → Paddle → RLM Cloud chạy thông trên sandbox.
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
- Đã có tài khoản Paddle (MoR active) và **Reprise RLM Cloud** (đã có ISV account + product/license template).
- Tích hợp web↔RLM Cloud qua **REST/JSON Web Services API** (provision/activate/verify license).
- Cubism Editor đã/đang tích hợp RLM Cloud activation (chỉ cần verify client, không build lại).
- Dùng theme tùy biến trên Gutenberg (không phải page builder nặng).
- Store hiện hành (store.live2d.com) **đã chạy WordPress** (theme Live2DStore) **+ plugin EC Welcart** (không phải WooCommerce — dấu hiệu `usces_page=login/newmember`). → Việc chuyển sang WooCommerce là **migration Welcart → WooCommerce** (khác plugin), schema account/order/license riêng → **Phase M nặng hơn**, cần khảo sát DB Welcart ở bước spec.
- Chức năng quản lý license trong My Page (xem key, deactivate/chuyển máy max 2 PC, order history, subscription, coupon student) **đã tồn tại** → build lại theo cái có (FR-16).
- Bản dịch nội dung (Phase L) do khách/vendor cung cấp, trừ khi chọn option dịch in-house.

**Rủi ro chính**
- **i18n-ready phải làm đúng từ đầu** — nếu hardcode chữ ở Phase 2, chi phí thêm ngôn ngữ sẽ đội lên nhiều.
- **Migration EN**: redirect/hreflang sai → mất SEO.
- **Đối soát doanh thu**: Paddle là MoR nên hóa đơn/thuế nằm ở Paddle, Woo chỉ là bản ghi nội bộ.
- **Idempotency webhook**: tránh tạo trùng license khi Paddle retry.
- **Mô hình license RLM Cloud** (license pool/activation key, provision theo product) khác hệ per-key — cần chốt mapping product↔license template ở giai đoạn spec, có thể ảnh hưởng MD Phase 4.
- **Migration Welcart → WooCommerce** (xem chi tiết §5b.1): khác plugin, **subscription đang active** (chuyển sang Paddle không gián đoạn), **license/activation đang dùng** (map sang RLM Cloud không khóa khách) — 3 điểm này phải khảo sát discovery sớm, là rủi ro lớn nhất của dự án.
- Chất lượng/khối lượng bản dịch có thể phát sinh thêm MD (đã có option/ghi chú ở Phase L).



# xxx — Screen Inventory & FR Traceability

> Mục đích: nối **Functional Requirements** (xxx-rebuild-plan.md §1) với **màn hình thực tế**
> trên xxx.com/en. Đọc 2 chiều: FR→Màn để biết FR nằm ở đâu; Màn→FR để biết 1 màn cần gì.

---

## A. Screen Inventory (danh sách màn hình)

### A0. Global (xuất hiện ở mọi màn)
| ID | Màn hình | Ghi chú |
|----|----------|---------|
| G-01 | Header + Mega menu | Products/Services/Learn/Communities/Support |
| G-02 | Footer nhiều cột | docs, services, support, legal, company |
| G-03 | Language switcher | 7 ngôn ngữ (EN trước) |
| G-04 | Search overlay/results | tìm kiếm toàn site |
| G-05 | Cookie/GDPR consent | banner |

### A1. Marketing / Content
| ID | Màn hình | Nguồn trên site gốc |
|----|----------|---------------------|
| S-01 | Homepage | trang chủ (hero, 500+ titles, services, community, education, news) |
| S-02 | Cubism Editor — Overview | "What's Cubism Editor?" |
| S-03 | Cubism Editor — So sánh FREE/PRO | bảng version |
| S-04 | Cubism Editor — Spec | yêu cầu hệ thống |
| S-05 | Cubism Editor — Updates/Changelog | release notes |
| S-06 | Cubism SDK — Overview | giới thiệu SDK |
| S-07 | SDK Download (đa nền tảng) | Unity/Web/Native/Java/Unreal/Cocos |
| S-08 | Support tools | After Effects plugin, Photoshop script |
| S-09 | Try / Download (trial 42 ngày) | nút "Try xxx" → cấp **trial license** (cloud activate) |
| S-10 | Services promo (link ngoài) | **ĐÃ ĐIỀU TRA**: tất cả link ngoài — nizima→docs.nizima.com, nizima LIVE→nizimalive.com, ACTION→site.nizima-action.com, JUKU→juku.xxxcs.jp, Creative Studio→xxxcs.jp. Chỉ làm block quảng bá + outbound link, KHÔNG build trang nội bộ |

### A2. Learn / Community
| ID | Màn hình | |
|----|----------|---|
| S-11 | Learn hub | **ĐÃ ĐIỀU TRA**: Editor/SDK manual & tutorial → docs.xxx.com (ngoài, chỉ link). Chỉ **Sample Data** là trang nội bộ |
| S-11b | Sample Data (nội bộ) | trang tải sample/model trên xxx.com |
| S-12 | Communities directory | danh sách cộng đồng (nội bộ) |
| S-13 | Chapters / Discord | link cộng đồng (ngoài) |

### A3. Programs / Support
| ID | Màn hình | |
|----|----------|---|
| S-14 | Student Discount (info + form) | -76% |
| S-15 | Education Aid / LEAP (info + form) | free cho trường |
| S-16 | Creative Awards (info + submission) | |
| S-17 | Contact / Help center (form) | |
| S-18 | Company / About | |
| S-19 | Careers | |

### A4. News
| ID | Màn hình | |
|----|----------|---|
| S-20 | News/Event listing + filter category | Sale/News/Update/Event/Awards |
| S-21 | News/Event detail | |

### A5. Legal
| ID | Màn hình | |
|----|----------|---|
| S-22 | License Agreement | |
| S-23 | Privacy / Terms | |

### A6. Commerce (MỚI — thay cho external xxx Store)
| ID | Màn hình | |
|----|----------|---|
| S-24 | Shop / Product list | catalog WooCommerce |
| S-25 | Product detail (mua) | giá theo vùng, nút Buy |
| S-26 | Cart | giỏ hàng |
| S-27 | Checkout (Paddle overlay) | Paddle.js popup, MoR/tax |
| S-28 | Order confirmation / Thank you | giao license sau mua |
| S-29 | My Account — Orders & Invoices | lịch sử + hóa đơn Paddle |
| S-30 | My Account — Licenses & Machines | xem key, activate/deactivate |
| S-31 | Auth (login/register/reset) | tài khoản |

### A7. System / Backend (không phải UI người dùng cuối)
| ID | Thành phần | |
|----|-----------|---|
| B-01 | Paddle webhook handler | verify signature + idempotency |
| B-02 | Reprise RLM Cloud integration service | tạo/suspend/revoke license |
| B-03 | Email service | license key + invoice link |
| B-04 | Admin/Editor (WP) phân quyền | team nội dung |

---

## B. Ma trận FR → Màn hình (mỗi FR nằm ở đâu)

| FR | Mô tả ngắn | Màn hình liên quan |
|----|-----------|--------------------|
| FR-01 | i18n-ready, EN trước | G-03 + toàn bộ S-* (kiến trúc) |
| FR-02 | Language switcher + locale URL + hreflang | G-03, mọi màn |
| FR-03 | Mega menu + footer | G-01, G-02 |
| FR-04 | Homepage blocks | S-01 |
| FR-05 | Product Editor/SDK + so sánh + spec | S-02, S-03, S-04, S-06 |
| FR-06 | Download SDK + trial + changelog | S-05, S-07, S-08, S-09 |
| FR-07 | News + filter category + detail | S-20, S-21 |
| FR-08 | Learn / Communities | S-11, S-12, S-13 |
| FR-09 | Forms (Contact/Student/LEAP/Awards) | S-14, S-15, S-16, S-17 |
| FR-10 | WooCommerce catalog + product↔Paddle Price | S-24, S-25 |
| FR-11 | Paddle overlay checkout (MoR/tax) | S-27, B-01 |
| FR-12 | Localized pricing + subscription | S-25, S-27 |
| FR-13 | Order sync Woo↔Paddle + webhook | S-28, S-29, B-01 |
| FR-14 | Tạo license theo policy | S-28, B-01, B-02, B-03 |
| FR-15 | Refund/revoke + trial expiry | S-30, B-01, B-02 |
| FR-16 | My Account license dashboard | S-29, S-30, S-31 |
| FR-17 | Editor activate/validate qua **Reprise RLM Cloud** (cloud activation) | B-02 (+ client Cubism Editor) |
| FR-18 | Phân quyền editor nội dung | B-04 |
| FR-19 | Site search | G-04 |
| FR-20 | Account/Auth (đăng ký/đăng nhập/reset) | S-31 |

> **Đã chốt**: Services (S-10) và phần lớn Learn (S-11) chỉ là **outbound link** → không build trang nội bộ.

---

## C. Ma trận Màn hình → FR (mỗi màn cần chức năng gì)

| Màn hình | FR cần có |
|----------|-----------|
| G-01/02 Header/Footer | FR-03, FR-02 |
| G-03 Language switcher | FR-01, FR-02 |
| G-04 Search | FR-19 |
| S-01 Homepage | FR-04, FR-03, FR-07 (news feed) |
| S-02–04 Editor pages | FR-05 |
| S-05/07/08/09 Download/Trial | FR-06, FR-14 (cấp trial license, cloud activate) |
| S-10 Services | outbound link (không FR nội bộ) |
| S-11 Learn | outbound link; **S-11b Sample Data** = FR-08 (nội bộ) |
| S-12–13 Community | FR-08 |
| S-14–16 Programs | FR-09, + cấp license edu/student (FR-14) |
| S-17 Contact | FR-09 |
| S-20/21 News | FR-07 |
| S-22/23 Legal | (nội dung tĩnh — đa ngôn ngữ FR-02) |
| S-24/25 Shop/Product | FR-10, FR-12 |
| S-26 Cart | FR-10 |
| S-27 Checkout | FR-11, FR-12, FR-13 |
| S-28 Thank you | FR-13, FR-14, FR-16 |
| S-29 Orders/Invoices | FR-13, FR-16 |
| S-30 Licenses/Machines | FR-15, FR-16, FR-17 |
| S-31 Auth | FR-20 |

---

## D. Gap — ĐÃ CHỐT (cập nhật theo quyết định)

| # | Vấn đề | Quyết định |
|---|--------|-----------|
| 1 | Search chưa có FR | ✅ Thêm **FR-19: Site search** |
| 2 | Auth/Account chưa có FR | ✅ Thêm **FR-20: Account/Auth** (đăng ký/đăng nhập/reset) |
| 3 | Trial download | ✅ **Cấp trial license**. License + activation dùng **Reprise RLM Cloud** (RLM Cloud là hệ phát hành license & cloud activation cho Cubism Editor). |
| 4 | Services (nizima/JUKU…) | ✅ Đã điều tra: **toàn bộ link ngoài** → chỉ block quảng bá + outbound link, giữ như cũ |
| 5 | Learn/manual | ✅ Đã điều tra: manual/tutorial → **docs.xxx.com (link ngoài)**; chỉ **Sample Data** nội bộ — giữ như cũ |
| 6 | Cart đa món vs đơn lẻ | ✅ **ĐÃ ĐIỀU TRA store.xxx.com — chốt single-item**. Store hiện hành chỉ 1 sản phẩm (Cubism PRO), variant = tier/plan, seat = quantity, KHÔNG có cart đa món. Xem mục F |
| 7 | Migration user/đơn cũ | ✅ **Giả định CÓ migration**, **báo giá riêng** (xem plan §Migration) |

---

## F. Xác nhận D6 — Single-item checkout (ĐÃ ĐIỀU TRA store.xxx.com)

**Bằng chứng từ store hiện hành (store.xxx.com/en):**
- Nền tảng: **WordPress** (theme `wp-content/themes/xxxStore/`).
- Chỉ **1 sản phẩm: Cubism PRO**.
- Biến thể: 3 tier (Indie/Business/Student) × plan (Monthly/Annual/3-Year).
- Có **quantity selector** (mua nhiều seat = quantity).
- **Không có cart đa sản phẩm** — thiết kế single-product + quantity.
- Subscription, không refund.

**→ Chốt: single-item checkout**, khớp đúng hành vi hiện hành.

Mô hình dữ liệu đề xuất (khớp store cũ):
- **1 WooCommerce product = Cubism PRO**; **variant (tier × plan)** = variations/Paddle Price ID; **seat = quantity**.
- Nút "Buy" → chọn tier/plan/quantity → mở thẳng **Paddle overlay** (1 transaction = 1 price × qty).
- Có thể **bỏ trang Cart (S-26)** hoặc giữ tối giản — đúng như store hiện tại.
- License RLM Cloud provision theo order item (1 món → mapping order↔license↔activation đơn giản).

⚠️ Ràng buộc: nếu **tương lai** thêm sản phẩm khác loại (add-on/SDK trả phí) → cần đánh giá lại có cần multi-item không. Hiện tại: KHÔNG, khóa single-item.

---

## G. Cách dùng tài liệu này

1. Toàn bộ gap mục D **đã chốt 100%** (D6 đã xác nhận qua điều tra store.xxx.com) → FR khớp đủ với màn hình.
2. Dùng **ma trận C** làm checklist khi thiết kế từng wireframe.
3. Dùng **ma trận B** để verify không FR nào bị bỏ sót màn.
4. Gắn mỗi màn vào sitemap để estimate UI/UX theo màn.

