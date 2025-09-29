# Staff Attendance and Leave Management System

## 📌 Overview

The **Staff Attendance and Leave Management System** is a web-based application designed for schools to efficiently track staff attendance and manage leave requests. The system replaces manual processes (paper registers, spreadsheets, verbal approvals) with a structured, digital solution that improves accuracy, transparency, and efficiency.

---

## 🎯 Objectives

* Provide staff with an easy way to mark attendance and apply for leave.
* Allow administrators to manage attendance records and approve/reject leave requests.
* Generate reports that help school management monitor staff performance and leave trends.
* Ensure secure role-based access (Staff vs Admin). Admins are created via a backend management command, while staff are invited by admins via email.
* Implement notifications to keep staff and admins informed of important actions.

---

## ✅ Implemented Features

### 🌐 General / Common

* **Role-Based Authentication:** Users can log in; roles include `staff` and `admin`.
* **Password Reset / Forgot Password:** Users can securely reset their password via email.
* **Profile Management:** Users can view and manage profile information including profile image, email, phone number, location, and date joined.

### 👤 Staff (Teachers/Non-Academic Staff)

* **Dashboard:** Displays attendance summary (present, absent, late) and pending leave requests.
* **Mark Attendance:** Staff can mark themselves as `present`, `absent`, or `late`.
* **Attendance History:** Staff can view a record of their past attendance.
* **Apply for Leave:** Staff can submit leave requests specifying leave type, start/end dates.
* **Track Leave Requests:** Staff can see the status of their submitted leave requests (pending, approved, rejected).
* **Notifications:** Staff receive notifications when their leave request is approved or rejected.

### 🔹 Admin (Principal/HR)

* **Admin Dashboard:**

  * Summary cards showing total staff, present today, absent today, late today, and pending leaves.
  * Attendance overview chart for the last 7 days with trends for Present, Absent, and Late.
  * Quick actions: Invite staff, approve leave requests, view attendance report, manage staff.
  * Recent leave requests table.
* **Manage Staff:** Admins can view and manage all staff accounts.
* **Attendance Reports:** Admins can view attendance reports for staff and filter by date range (7, 14, 21, 30, 90 days).
* **Leave Management:** Admins can approve or reject leave requests and view leave history.
* **Notifications:** Admins receive notifications when staff apply for leave.

### 🛠 Backend & System Functionality

* **Attendance Model:** Tracks `staff`, `date`, `status` (present/absent/late), and timestamp; ensures one record per staff per day.
* **Leave Model:** Tracks leave requests with `staff`, `leave_type`, `start_date`, `end_date`, `status`, and timestamp.
* **Email-Based Staff Invitations:** Admins can invite staff via email to join the system.
* **Chart.js Integration:** Admin dashboard shows attendance trends in a responsive line chart.
* **Secure Role Access:** Staff cannot access admin-only features; admin cannot access staff-only features.
* **Functional Notifications System:** Real-time notifications for leave approvals, rejections, and staff actions.

### 🛠 Tech Stack (Implemented)

* **Backend:** Python, Django
* **Frontend:** HTML, CSS, Bootstrap 5, JavaScript
* **Database:** SQLite (development), ready for PostgreSQL (production)
* **Other Tools:** Django Authentication, Chart.js for trends visualization

---

✅ This document reflects the completed functionality of the project.

---

