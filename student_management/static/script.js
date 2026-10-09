
const form = document.getElementById("student-form");
const message = document.getElementById("message");
const studentsList = document.getElementById("students-list");
const averageResult = document.getElementById("average-result");

async function loadStudents() {
    const response = await fetch("/api/students");
    const students = await response.json();

    studentsList.replaceChildren();

    students.forEach(student => {
        const row = document.createElement("tr");

        [student.id, student.name, student.grade].forEach(value => {
            const cell = document.createElement("td");
            cell.textContent = value;
            row.appendChild(cell);
        });

        studentsList.appendChild(row);
    });
}

form.addEventListener("submit", async event => {
    event.preventDefault();

    message.textContent = "";

    try {
        const response = await fetch("/api/students", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                name: document.getElementById("name").value,
                grade: document.getElementById("grade").value
            })
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || "حدث خطأ.");
        }

        message.textContent = result.message;
        form.reset();
        await loadStudents();
        averageResult.textContent = "";
    } catch (error) {
        message.textContent = error.message;
    }
});

document.getElementById("average-button")
    .addEventListener("click", async () => {
        try {
            const response = await fetch("/api/average");
            const result = await response.json();

            averageResult.textContent = result.count === 0
                ? "لا توجد علامات لحساب المتوسط."
                : `متوسط العلامات: ${result.average}`;
        } catch {
            averageResult.textContent = "تعذر الاتصال بالخادم.";
        }
    });

loadStudents().catch(() => {
    message.textContent = "تعذر تحميل قائمة الطلاب.";
});