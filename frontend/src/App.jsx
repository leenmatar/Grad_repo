import { useEffect, useState } from "react";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Legend,
} from "recharts";

import "./App.css";


function App() {

  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");

  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);

  const [tickets, setTickets] = useState([]);
  const [ticketHistory, setTicketHistory] = useState([]);

  const [categoryId, setCategoryId] = useState("");
  const [priority, setPriority] = useState("");
  const [status, setStatus] = useState("");

  const [selectedTicket, setSelectedTicket] = useState(null);

  const [similarTickets, setSimilarTickets] = useState([]);

  const [statusHistory, setStatusHistory] = useState([]);

  // NEW: Saved AI analysis
  const [ticketAnalysis, setTicketAnalysis] = useState([]);

  const [stats, setStats] = useState(null);

  const [editingTicket, setEditingTicket] = useState(null);

  const [editTitle, setEditTitle] = useState("");
  const [editDescription, setEditDescription] = useState("");
  const [editPriority, setEditPriority] = useState("");
  const [editStatus, setEditStatus] = useState("");


  // -----------------------------
  // Load Tickets
  // -----------------------------

  const loadTickets = async () => {

    try {

      const response = await fetch(
        "http://127.0.0.1:8000/api/tickets"
      );

      const data = await response.json();

      setTickets(data);

    } catch (error) {

      console.error(
        "Error loading tickets:",
        error
      );

    }

  };


  // -----------------------------
  // Load User Ticket History
  // -----------------------------

  const loadTicketHistory = async () => {

    try {

      const response = await fetch(
        "http://127.0.0.1:8000/api/users/1/tickets"
      );

      const data = await response.json();

      setTicketHistory(data);

    } catch (error) {

      console.error(
        "Error loading ticket history:",
        error
      );

    }

  };


  // -----------------------------
  // Load Dashboard Statistics
  // -----------------------------

  const loadStats = async () => {

    try {

      const response = await fetch(
        "http://127.0.0.1:8000/api/dashboard/stats"
      );

      const data = await response.json();

      setStats(data);

    } catch (error) {

      console.error(
        "Error loading dashboard stats:",
        error
      );

    }

  };


  // -----------------------------
  // Load Status History
  // -----------------------------

  const loadStatusHistory = async (ticketId) => {

    try {

      const response = await fetch(
        `http://127.0.0.1:8000/api/tickets/${ticketId}/history`
      );

      if (!response.ok) {

        setStatusHistory([]);

        return;

      }

      const data = await response.json();

      setStatusHistory(
        data.status_history || []
      );

    } catch (error) {

      console.error(
        "Error loading status history:",
        error
      );

      setStatusHistory([]);

    }

  };


  // -----------------------------
  // Load Saved AI Analysis
  // -----------------------------

  const loadTicketAnalysis = async (ticketId) => {

    try {

      const response = await fetch(
        `http://127.0.0.1:8000/api/tickets/${ticketId}/analysis`
      );

      if (!response.ok) {

        setTicketAnalysis([]);

        return;

      }

      const data = await response.json();

      setTicketAnalysis(
        data.analysis || []
      );

    } catch (error) {

      console.error(
        "Error loading ticket analysis:",
        error
      );

      setTicketAnalysis([]);

    }

  };


  // -----------------------------
  // Initial Loading
  // -----------------------------

  useEffect(() => {

    loadTickets();

    loadTicketHistory();

    loadStats();

  }, []);


  // -----------------------------
  // Submit Ticket
  // -----------------------------

  const submitTicket = async (event) => {

    event.preventDefault();

    setLoading(true);

    setAnalysis(null);

    try {

      const response = await fetch(
        "http://127.0.0.1:8000/api/tickets",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({

            user_id: 1,

            title: title,

            description: description,

          }),

        }
      );

      const data = await response.json();

      setAnalysis(data);

      if (response.ok) {

        setTitle("");

        setDescription("");

        await loadTickets();

        await loadTicketHistory();

        await loadStats();

      }

    } catch (error) {

      console.error(
        "Error submitting ticket:",
        error
      );

    } finally {

      setLoading(false);

    }

  };


  // -----------------------------
  // Filter Tickets
  // -----------------------------

  const filterTicketList = async () => {

    const params = new URLSearchParams();

    if (categoryId) {

      params.append(
        "category_id",
        categoryId
      );

    }

    if (priority) {

      params.append(
        "priority",
        priority
      );

    }

    if (status) {

      params.append(
        "status",
        status
      );

    }

    try {

      const response = await fetch(
        `http://127.0.0.1:8000/api/tickets/filter/?${params.toString()}`
      );

      const data = await response.json();

      setTickets(data);

    } catch (error) {

      console.error(
        "Error filtering tickets:",
        error
      );

    }

  };


  // -----------------------------
  // Clear Filters
  // -----------------------------

  const clearFilters = () => {

    setCategoryId("");

    setPriority("");

    setStatus("");

    loadTickets();

  };


  // -----------------------------
  // View Ticket
  // -----------------------------

  const viewTicket = async (ticketId) => {

    try {

      // Ticket details
      const ticketResponse = await fetch(
        `http://127.0.0.1:8000/api/tickets/${ticketId}`
      );

      const ticketData =
        await ticketResponse.json();

      setSelectedTicket(ticketData);


      // Similar tickets
      const similarResponse = await fetch(
        `http://127.0.0.1:8000/api/tickets/${ticketId}/similar`
      );

      const similarData =
        await similarResponse.json();

      setSimilarTickets(
        similarData.similar_tickets || []
      );


      // Status history
      await loadStatusHistory(ticketId);


      // Saved AI analysis
      await loadTicketAnalysis(ticketId);

    } catch (error) {

      console.error(
        "Error loading ticket details:",
        error
      );

    }

  };


  // -----------------------------
  // Close Ticket Details
  // -----------------------------

  const closeTicketDetails = () => {

    setSelectedTicket(null);

    setSimilarTickets([]);

    setStatusHistory([]);

    setTicketAnalysis([]);

  };


  // -----------------------------
  // Delete Ticket
  // -----------------------------

  const deleteTicket = async (ticketId) => {

    const confirmed = window.confirm(
      "Are you sure you want to delete this ticket?"
    );

    if (!confirmed) {

      return;

    }

    try {

      const response = await fetch(
        `http://127.0.0.1:8000/api/tickets/${ticketId}`,
        {
          method: "DELETE",
        }
      );

      if (response.ok) {

        await loadTickets();

        await loadTicketHistory();

        await loadStats();


        if (
          selectedTicket &&
          selectedTicket.ticket_id === ticketId
        ) {

          closeTicketDetails();

        }


        if (
          editingTicket &&
          editingTicket.ticket_id === ticketId
        ) {

          setEditingTicket(null);

        }

      }

    } catch (error) {

      console.error(
        "Error deleting ticket:",
        error
      );

    }

  };


  // -----------------------------
  // Start Editing Ticket
  // -----------------------------

  const startEditTicket = (ticket) => {

    setEditingTicket(ticket);

    setEditTitle(ticket.title);

    setEditDescription(
      ticket.description
    );

    setEditPriority(ticket.priority);

    setEditStatus(ticket.status);

  };


  // -----------------------------
  // Save Edited Ticket
  // -----------------------------

  const saveEditTicket = async (event) => {

    event.preventDefault();

    if (!editingTicket) {

      return;

    }

    const editingTicketId =
      editingTicket.ticket_id;

    try {

      const response = await fetch(
        `http://127.0.0.1:8000/api/tickets/${editingTicketId}`,
        {
          method: "PUT",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({

            title: editTitle,

            description:
              editDescription,

            priority:
              editPriority,

            status:
              editStatus,

          }),

        }
      );

      if (response.ok) {

        setEditingTicket(null);

        await loadTickets();

        await loadTicketHistory();

        await loadStats();


        if (
          selectedTicket &&
          selectedTicket.ticket_id ===
            editingTicketId
        ) {

          await viewTicket(
            editingTicketId
          );

        }

      } else {

        const data =
          await response.json();

        console.error(
          "Update failed:",
          data
        );

      }

    } catch (error) {

      console.error(
        "Error updating ticket:",
        error
      );

    }

  };


  // -----------------------------
  // Format Date
  // -----------------------------

  const formatDate = (dateValue) => {

    if (!dateValue) {

      return "-";

    }

    const date =
      new Date(dateValue);

    return date.toLocaleString();

  };


  // -----------------------------
  // Dashboard Chart Data
  // -----------------------------

  const categoryChartData = stats
    ? Object.entries(
        stats.tickets_by_category
      ).map(
        ([name, value]) => ({
          name,
          value,
        })
      )
    : [];


  const priorityChartData = stats
    ? Object.entries(
        stats.tickets_by_priority
      ).map(
        ([name, value]) => ({
          name,
          value,
        })
      )
    : [];


  const statusChartData = stats
    ? [

        {
          name: "Open",
          value:
            stats.open_tickets,
        },

        {
          name: "Resolved",
          value:
            stats.resolved_tickets,
        },

      ]
    : [];


  const pieColors = [

    "#8884d8",

    "#82ca9d",

    "#ffc658",

    "#ff8042",

    "#0088fe",

  ];


  return (

    <div className="app">


      {/* Header */}

      <h1>
        AI Support Ticket Intelligence Platform
      </h1>


      <p className="subtitle">
        Submit your technical issue and let AI
        analyze it.
      </p>


      {/* Dashboard */}

      {stats && (

        <div className="dashboard">

          <h2>
            Dashboard
          </h2>


          <div className="stat-cards">

            <div className="stat-card">

              <h3>
                Total Tickets
              </h3>

              <p>
                {stats.total_tickets}
              </p>

            </div>


            <div className="stat-card">

              <h3>
                Open Tickets
              </h3>

              <p>
                {stats.open_tickets}
              </p>

            </div>


            <div className="stat-card">

              <h3>
                Resolved Tickets
              </h3>

              <p>
                {stats.resolved_tickets}
              </p>

            </div>

          </div>


          <div className="charts-container">


            {/* Category Chart */}

            <div className="chart-card">

              <h3>
                Tickets by Category
              </h3>

              <ResponsiveContainer
                width="100%"
                height={300}
              >

                <BarChart
                  data={
                    categoryChartData
                  }
                >

                  <XAxis
                    dataKey="name"
                  />

                  <YAxis
                    allowDecimals={false}
                  />

                  <Tooltip />

                  <Bar
                    dataKey="value"
                    fill="#8884d8"
                  />

                </BarChart>

              </ResponsiveContainer>

            </div>


            {/* Priority Chart */}

            <div className="chart-card">

              <h3>
                Tickets by Priority
              </h3>

              <ResponsiveContainer
                width="100%"
                height={300}
              >

                <PieChart>

                  <Pie
                    data={
                      priorityChartData
                    }
                    dataKey="value"
                    nameKey="name"
                    outerRadius={90}
                    label
                  >

                    {priorityChartData.map(
                      (entry, index) => (

                        <Cell
                          key={
                            entry.name
                          }
                          fill={
                            pieColors[
                              index %
                              pieColors.length
                            ]
                          }
                        />

                      )
                    )}

                  </Pie>

                  <Tooltip />

                  <Legend />

                </PieChart>

              </ResponsiveContainer>

            </div>


            {/* Status Chart */}

            <div className="chart-card">

              <h3>
                Ticket Status
              </h3>

              <ResponsiveContainer
                width="100%"
                height={300}
              >

                <BarChart
                  data={
                    statusChartData
                  }
                >

                  <XAxis
                    dataKey="name"
                  />

                  <YAxis
                    allowDecimals={false}
                  />

                  <Tooltip />

                  <Bar
                    dataKey="value"
                    fill="#82ca9d"
                  />

                </BarChart>

              </ResponsiveContainer>

            </div>

          </div>

        </div>

      )}


      {/* Submit Ticket */}

      <div className="ticket-form-container">

        <h2>
          Submit Ticket
        </h2>


        <form
          onSubmit={submitTicket}
        >

          <label>
            Title
          </label>

          <input
            type="text"
            value={title}
            onChange={(event) =>
              setTitle(
                event.target.value
              )
            }
            placeholder="Enter ticket title"
            required
          />


          <label>
            Description
          </label>

          <textarea
            value={description}
            onChange={(event) =>
              setDescription(
                event.target.value
              )
            }
            placeholder="Describe your technical problem"
            rows="6"
            required
          />


          <button type="submit">

            {loading
              ? "Submitting..."
              : "Submit Ticket"}

          </button>

        </form>

      </div>


      {/* AI Analysis */}

      {analysis && (

        <div className="analysis-result">

          <h2>
            Ticket Analysis
          </h2>


          {analysis.predicted_category && (

            <>

              <p>

                <strong>
                  Predicted Category:
                </strong>{" "}

                {
                  analysis.predicted_category
                }

              </p>


              <p>

                <strong>
                  Confidence:
                </strong>{" "}

                {
                  Number(
                    analysis.confidence
                  ).toFixed(2)
                }%

              </p>


              <p>

                <strong>
                  Priority:
                </strong>{" "}

                {
                  analysis.priority
                }

              </p>


              <p>

                <strong>
                  Ticket ID:
                </strong>{" "}

                {
                  analysis.ticket_id
                }

              </p>

            </>

          )}


          {analysis.detail && (

            <p>
              {analysis.detail}
            </p>

          )}

        </div>

      )}


      {/* Tickets */}

      <div className="ticket-list-container">

        <h2>
          Tickets
        </h2>


        {/* Filters */}

        <div className="filters">


          <select
            value={categoryId}
            onChange={(event) =>
              setCategoryId(
                event.target.value
              )
            }
          >

            <option value="">
              All Categories
            </option>

            <option value="1">
              Account
            </option>

            <option value="2">
              Network
            </option>

            <option value="3">
              Software
            </option>

            <option value="4">
              Hardware
            </option>

            <option value="5">
              Academic System
            </option>

          </select>


          <select
            value={priority}
            onChange={(event) =>
              setPriority(
                event.target.value
              )
            }
          >

            <option value="">
              All Priorities
            </option>

            <option value="Low">
              Low
            </option>

            <option value="Medium">
              Medium
            </option>

            <option value="High">
              High
            </option>

            <option value="Critical">
              Critical
            </option>

          </select>


          <select
            value={status}
            onChange={(event) =>
              setStatus(
                event.target.value
              )
            }
          >

            <option value="">
              All Statuses
            </option>

            <option value="Open">
              Open
            </option>

            <option value="In Progress">
              In Progress
            </option>

            <option value="Resolved">
              Resolved
            </option>

          </select>


          <button
            onClick={
              filterTicketList
            }
          >
            Apply Filters
          </button>


          <button
            onClick={clearFilters}
          >
            Clear Filters
          </button>

        </div>


        {/* Ticket Table */}

        {tickets.length === 0 ? (

          <p>
            No tickets found.
          </p>

        ) : (

          <table>

            <thead>

              <tr>

                <th>
                  ID
                </th>

                <th>
                  Title
                </th>

                <th>
                  Priority
                </th>

                <th>
                  Status
                </th>

                <th>
                  Actions
                </th>

              </tr>

            </thead>


            <tbody>

              {tickets.map(
                (ticket) => (

                  <tr
                    key={
                      ticket.ticket_id
                    }
                  >

                    <td>
                      {
                        ticket.ticket_id
                      }
                    </td>

                    <td>
                      {
                        ticket.title
                      }
                    </td>

                    <td>
                      {
                        ticket.priority
                      }
                    </td>

                    <td>
                      {
                        ticket.status
                      }
                    </td>

                    <td>

                      <button
                        onClick={() =>
                          viewTicket(
                            ticket.ticket_id
                          )
                        }
                      >
                        View
                      </button>


                      <button
                        onClick={() =>
                          startEditTicket(
                            ticket
                          )
                        }
                      >
                        Edit
                      </button>


                      <button
                        onClick={() =>
                          deleteTicket(
                            ticket.ticket_id
                          )
                        }
                      >
                        Delete
                      </button>

                    </td>

                  </tr>

                )
              )}

            </tbody>

          </table>

        )}

      </div>


      {/* My Ticket History */}

      <div className="ticket-list-container">

        <h2>
          My Ticket History
        </h2>


        <p>
          Tickets submitted by User 1,
          ordered from newest to oldest.
        </p>


        {ticketHistory.length === 0 ? (

          <p>
            No ticket history found.
          </p>

        ) : (

          <table>

            <thead>

              <tr>

                <th>
                  ID
                </th>

                <th>
                  Title
                </th>

                <th>
                  Priority
                </th>

                <th>
                  Status
                </th>

                <th>
                  Created At
                </th>

                <th>
                  Action
                </th>

              </tr>

            </thead>


            <tbody>

              {ticketHistory.map(
                (ticket) => (

                  <tr
                    key={
                      ticket.ticket_id
                    }
                  >

                    <td>
                      {
                        ticket.ticket_id
                      }
                    </td>

                    <td>
                      {
                        ticket.title
                      }
                    </td>

                    <td>
                      {
                        ticket.priority
                      }
                    </td>

                    <td>
                      {
                        ticket.status
                      }
                    </td>

                    <td>
                      {
                        formatDate(
                          ticket.created_at
                        )
                      }
                    </td>

                    <td>

                      <button
                        onClick={() =>
                          viewTicket(
                            ticket.ticket_id
                          )
                        }
                      >
                        View
                      </button>

                    </td>

                  </tr>

                )
              )}

            </tbody>

          </table>

        )}

      </div>


      {/* Edit Ticket */}

      {editingTicket && (

        <div className="ticket-details">

          <h2>
            Edit Ticket
          </h2>


          <form
            onSubmit={
              saveEditTicket
            }
          >

            <label>
              Title
            </label>

            <input
              type="text"
              value={editTitle}
              onChange={(event) =>
                setEditTitle(
                  event.target.value
                )
              }
              required
            />


            <label>
              Description
            </label>

            <textarea
              value={editDescription}
              onChange={(event) =>
                setEditDescription(
                  event.target.value
                )
              }
              rows="5"
              required
            />


            <label>
              Priority
            </label>

            <select
              value={editPriority}
              onChange={(event) =>
                setEditPriority(
                  event.target.value
                )
              }
            >

              <option value="Low">
                Low
              </option>

              <option value="Medium">
                Medium
              </option>

              <option value="High">
                High
              </option>

              <option value="Critical">
                Critical
              </option>

            </select>


            <label>
              Status
            </label>

            <select
              value={editStatus}
              onChange={(event) =>
                setEditStatus(
                  event.target.value
                )
              }
            >

              <option value="Open">
                Open
              </option>

              <option value="In Progress">
                In Progress
              </option>

              <option value="Resolved">
                Resolved
              </option>

            </select>


            <button type="submit">
              Save Changes
            </button>


            <button
              type="button"
              onClick={() =>
                setEditingTicket(null)
              }
            >
              Cancel
            </button>

          </form>

        </div>

      )}


      {/* Ticket Details */}

      {selectedTicket && (

        <div className="ticket-details">

          <h2>
            Ticket Details
          </h2>


          <p>

            <strong>
              ID:
            </strong>{" "}

            {
              selectedTicket.ticket_id
            }

          </p>


          <p>

            <strong>
              Title:
            </strong>{" "}

            {
              selectedTicket.title
            }

          </p>


          <p>

            <strong>
              Description:
            </strong>{" "}

            {
              selectedTicket.description
            }

          </p>


          <p>

            <strong>
              Priority:
            </strong>{" "}

            {
              selectedTicket.priority
            }

          </p>


          <p>

            <strong>
              Status:
            </strong>{" "}

            {
              selectedTicket.status
            }

          </p>


          {/* -------------------------------- */}
          {/* AI Analysis */}
          {/* -------------------------------- */}

          <h3>
            AI Analysis
          </h3>


          {ticketAnalysis.length === 0 ? (

            <p>
              No saved AI analysis found.
            </p>

          ) : (

            <div className="ai-analysis">

              {ticketAnalysis.map(
                (savedAnalysis) => (

                  <div
                    key={
                      savedAnalysis.analysis_id
                    }
                  >

                    <p>

                      <strong>
                        Predicted Category:
                      </strong>{" "}

                      {
                        savedAnalysis.category_name
                      }

                    </p>


                    <p>

                      <strong>
                        Confidence:
                      </strong>{" "}

                      {
                        Number(
                          savedAnalysis.confidence_score
                        ).toFixed(2)
                      }%

                    </p>


                    <p>

                      <strong>
                        Detected Priority:
                      </strong>{" "}

                      {
                        savedAnalysis.detected_priority
                      }

                    </p>


                    <p>

                      <strong>
                        Analyzed At:
                      </strong>{" "}

                      {
                        formatDate(
                          savedAnalysis.created_at
                        )
                      }

                    </p>

                  </div>

                )
              )}

            </div>

          )}


          {/* -------------------------------- */}
          {/* Status History */}
          {/* -------------------------------- */}

          <h3>
            Status History
          </h3>


          {statusHistory.length === 0 ? (

            <p>
              No status history found.
            </p>

          ) : (

            <div className="status-history">

              {statusHistory.map(
                (history, index) => (

                  <div
                    className="status-history-item"
                    key={
                      history.history_id
                    }
                  >

                    <p>

                      <strong>
                        {history.new_status}
                      </strong>

                    </p>


                    {history.old_status && (

                      <p>

                        {history.old_status}
                        {" → "}
                        {history.new_status}

                      </p>

                    )}


                    {!history.old_status && (

                      <p>
                        Ticket created
                      </p>

                    )}


                    <p>

                      <small>
                        {
                          formatDate(
                            history.changed_at
                          )
                        }
                      </small>

                    </p>


                    {index <
                      statusHistory.length - 1 && (

                      <hr />

                    )}

                  </div>

                )
              )}

            </div>

          )}


          {/* -------------------------------- */}
          {/* Similar Tickets */}
          {/* -------------------------------- */}

          <h3>
            Similar Resolved Tickets
          </h3>


          {similarTickets.length === 0 ? (

            <p>
              No similar tickets found.
            </p>

          ) : (

            <div>

              {similarTickets.map(
                (ticket) => (

                  <div
                    className="similar-ticket"
                    key={
                      ticket.ticket_id
                    }
                  >

                    <h4>
                      {
                        ticket.title
                      }
                    </h4>


                    <p>
                      {
                        ticket.description
                      }
                    </p>


                    <p>

                      <strong>
                        Similarity:
                      </strong>{" "}

                      {
                        ticket.similarity
                      }%

                    </p>


                    <p>

                      <strong>
                        Verified Solution:
                      </strong>{" "}

                      {
                        ticket.solution
                      }

                    </p>

                  </div>

                )
              )}

            </div>

          )}


          <button
            onClick={
              closeTicketDetails
            }
          >
            Close
          </button>

        </div>

      )}

    </div>

  );

}


export default App;