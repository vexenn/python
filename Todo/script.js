class VutsDashboard {
  constructor() {
    this.tickets = [];
    this.filter = "all";
    this.selectedDate = "";
    this.activeResolveId = null;

    // DOM Elements
    this.form = document.getElementById("ticketForm");
    this.titleInput = document.getElementById("titleInput");
    this.requestorInput = document.getElementById("requestorInput");
    this.assigneeInput = document.getElementById("assigneeInput");
    this.priorityInput = document.getElementById("priorityInput");
    this.calendarInput = document.getElementById("calendarInput");
    
    this.ticketList = document.getElementById("ticketList");
    this.emptyState = document.getElementById("emptyState");
    this.formError = document.getElementById("formError");
    this.filterButtons = document.querySelectorAll(".filter-btn");
    this.toast = document.getElementById("toast");

    // Modal Elements
    this.resolveModal = document.getElementById("resolveModal");
    this.resolveComment = document.getElementById("resolveComment");
    this.confirmResolveBtn = document.getElementById("confirmResolve");
    this.cancelResolveBtn = document.getElementById("cancelResolve");

    this.bindEvents();
    this.fetchTickets();
  }

  bindEvents() {
    this.form.addEventListener("submit", (e) => {
      e.preventDefault();
      this.createTicket();
    });

    this.calendarInput.addEventListener("change", (e) => {
      this.selectedDate = e.target.value;
      this.fetchTickets();
    });

    this.ticketList.addEventListener("click", (e) => {
      const item = e.target.closest(".task-item");
      if (!item) return;
      const ticketId = item.dataset.id;

      if (e.target.classList.contains("btn-resolve-trigger")) {
        this.openResolveModal(ticketId);
      }
      if (e.target.closest(".delete-btn")) {
        this.deleteTicket(ticketId);
      }
    });

    this.cancelResolveBtn.addEventListener("click", () => this.closeResolveModal());
    this.confirmResolveBtn.addEventListener("click", () => this.handleResolveConfirm());

    this.filterButtons.forEach(btn => {
      btn.addEventListener("click", () => {
        this.filter = btn.dataset.filter;
        this.filterButtons.forEach(b => {
          b.classList.remove("bg-cyan-500/20", "text-cyan-400", "border-cyan-500/50");
          b.classList.add("text-slate-400");
        });
        btn.classList.add("bg-cyan-500/20", "text-cyan-400", "border-cyan-500/50");
        btn.classList.remove("text-slate-400");
        this.render();
      });
    });
  }

  // --- API OPERATIONS ---

  async fetchTickets() {
    // Aligned to /api/tasks to match app.py
    let url = "/api/tasks"; 
    if (this.selectedDate) url += `?date=${this.selectedDate}`;

    try {
      const response = await fetch(url);
      if (!response.ok) throw new Error();
      this.tickets = await response.json();
      this.render();
    } catch (err) {
      this.showToast("Error connecting to server");
    }
  }

  async createTicket() {
    const payload = {
      title: this.titleInput.value.trim(),
      requestor: this.requestorInput.value.trim(),
      assignee: this.assigneeInput.value.trim() || "Unassigned",
      priority: this.priorityInput.value,
      due_date: this.selectedDate || null
    };

    if (!payload.title || !payload.requestor) {
      this.formError.textContent = "Subject and Requestor are required.";
      return;
    }

    try {
      // Aligned to /api/tasks
      const response = await fetch("/api/tasks", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      if (response.ok) {
        this.form.reset();
        this.formError.textContent = "";
        this.fetchTickets();
        this.showToast("Ticket Created");
      }
    } catch (err) {
      this.showToast("Failed to create ticket");
    }
  }

  // --- RESOLVE WORKFLOW ---

  openResolveModal(ticketId) {
    this.activeResolveId = ticketId;
    this.resolveModal.classList.remove("hidden");
    this.resolveComment.focus();
  }

  closeResolveModal() {
    this.resolveModal.classList.add("hidden");
    this.resolveComment.value = "";
    this.activeResolveId = null;
  }

  async handleResolveConfirm() {
    const commentText = this.resolveComment.value.trim();
    if (!commentText) {
      alert("A resolution comment is required to close this ticket.");
      return;
    }

    try {
      // Endpoint maintained for specific resolve logic
      const response = await fetch(`/api/tickets/${this.activeResolveId}/resolve`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ comment: commentText })
      });

      if (response.ok) {
        this.showToast("Ticket Resolved!");
        this.closeResolveModal();
        this.fetchTickets();
      }
    } catch (err) {
      this.showToast("Failed to resolve ticket");
    }
  }

  async deleteTicket(id) {
    if (!confirm("Permanently delete this ticket?")) return;
    // Aligned to /api/tasks path
    const response = await fetch(`/api/tasks/${id}`, { method: "DELETE" });
    if (response.ok) {
      this.fetchTickets();
      this.showToast("Ticket Deleted");
    }
  }

  // --- RENDERING ---

  render() {
    const visible = this.getFilteredTickets();
    this.ticketList.innerHTML = "";

    visible.forEach(t => {
      const li = document.createElement("li");
      li.className = `task-item flex flex-col md:flex-row md:items-center justify-between bg-slate-800/40 p-4 rounded-2xl border border-slate-700/50 hover:bg-slate-800/60 transition-all ${t.is_resolved ? 'opacity-60' : ''}`;
      li.dataset.id = t.id;

      const pStyle = t.priority === "High" ? "text-red-400 border-red-400/20 bg-red-400/5" : 
                    t.priority === "Medium" ? "text-yellow-400 border-yellow-400/20 bg-yellow-400/5" : 
                    "text-blue-400 border-blue-400/20 bg-blue-400/5";

      li.innerHTML = `
        <div class="flex flex-col gap-1 mb-3 md:mb-0">
          <span class="font-bold ${t.is_resolved ? 'line-through text-slate-500' : 'text-slate-100'}">
            <span class="text-cyan-400 mr-2 opacity-70">#${t.id}</span>${t.title}
          </span>
          <div class="text-[10px] uppercase tracking-widest text-slate-500 font-black">
            Req: <span class="text-slate-300">${t.requestor}</span> | 
            Owner: <span class="text-slate-300">${t.assignee}</span>
          </div>
        </div>
        
        <div class="flex items-center justify-between md:justify-end gap-4">
          <span class="text-[10px] font-bold px-2 py-1 rounded border ${pStyle}">${t.priority}</span>
          ${!t.is_resolved 
            ? `<button class="btn-resolve-trigger bg-cyan-500 text-slate-900 text-[10px] font-black px-4 py-2 rounded-lg hover:bg-cyan-400 transition-all">RESOLVE</button>` 
            : '<span class="text-emerald-400 text-[10px] font-black uppercase tracking-tighter">Resolved ✅</span>'}
          <button class="delete-btn text-slate-600 hover:text-red-500 transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h18m-2 0v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6m3 0V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/></svg>
          </button>
        </div>
      `;
      this.ticketList.appendChild(li);
    });

    this.emptyState.classList.toggle("hidden", visible.length > 0);
  }

  getFilteredTickets() {
    return this.tickets.filter(t => {
      if (this.filter === "active") return !t.is_resolved;
      if (this.filter === "completed") return t.is_resolved;
      return true;
    });
  }

  showToast(msg) {
    this.toast.textContent = msg;
    this.toast.classList.replace("opacity-0", "opacity-100");
    setTimeout(() => {
      this.toast.classList.replace("opacity-100", "opacity-0");
    }, 2000);
  }
}

document.addEventListener("DOMContentLoaded", () => new VutsDashboard());
