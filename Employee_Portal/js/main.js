$(document).ready(function () {

    // Vis loginfelter
    $(".login-prev-btn").click(function () {
        $(".inputx").show(150);
        $(".login-prev-btn").hide();
    });

    // Dummy users
    const users = [
        {
            user_id: 1,
            email: "martin.hansen@dxc.com",
            password: "K9!vR2pQx7Lz",
            full_name: "Martin Hansen",
            department: "IT Operations",
            role: "Employee"
        },
        {
            user_id: 2,
            email: "sara.madsen@dxc.com",
            password: "1234",
            full_name: "Sara Madsen",
            department: "Finance",
            role: "Employee"
        }
    ];

    function getOrCreateDeviceId() {
        let deviceId = localStorage.getItem("deviceId");

        if (!deviceId) {
            deviceId = "device_" + crypto.randomUUID();
            localStorage.setItem("deviceId", deviceId);
        }

        return deviceId;
    }

    async function sendAuthLog(logData) {
        try {
            const response = await fetch("http://127.0.0.1:5000/api/logs", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(logData)
            });

            return await response.json();

        } catch (error) {
            console.error("Could not send log to backend:", error);
        }
    }

    // Login submit
    $("#formpass").submit(async function (event) {
        event.preventDefault();

        const username = $("input[name='username']").val().trim().toLowerCase();
        const password = $("input[name='password']").val().trim();

        const user = users.find(u =>
            u.email.toLowerCase() === username &&
            u.password === password
        );

        if (user) {

            // Gem den aktuelle bruger midlertidigt
            localStorage.setItem("currentUser", JSON.stringify(user));

            // Gem tidspunkt for login-start
            localStorage.setItem("loginStartTime", Date.now().toString());

            // Bruges senere til mfa_duration_ms
            localStorage.setItem("mfaStartTime", Date.now().toString());

            // Nulstil MFA attempts for denne login-session
            localStorage.setItem("mfaFailedAttempts", "0");

            // Redirect til MFA-side
            window.location.href = "mfa.html";

        } else {

            await sendAuthLog({
                user_id: username || "unknown_user",
                timestamp: new Date().toISOString(),
                ip: "frontend_test_ip",
                country: "Denmark",
                city: "Aarhus",
                device: "Browser",
                device_id: getOrCreateDeviceId(),
                device_type: "Desktop",
                browser: "Chrome",
                os: "Windows",
                user_agent: navigator.userAgent,
                event_type: "login_failure",
                login_status: "failed",
                login_duration_ms: 0,
                mfa_required: false,
                mfa_success: false,
                mfa_duration_ms: 0,
                failed_attempts_before_success: 1,
                session_id: "no_session",
                session_duration_minutes: 0
            });

            alert("Wrong username or password.");
        }
    });

});