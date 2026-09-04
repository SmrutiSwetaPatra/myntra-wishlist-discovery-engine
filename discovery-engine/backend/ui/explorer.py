import streamlit as st
from ui.db_utils import get_explorer_data, get_dashboard_metrics


def format_label(value, fallback="Unknown"):
    """Convert internal enum values into PM-friendly labels."""
    if not value:
        return fallback

    return str(value).replace("_", " ").title()


def render_explorer():
    st.title("🔎 Evidence Explorer")
    st.markdown("Explore the evidence behind product opportunities.")

    # -----------------------------------------
    # LOAD FILTER OPTIONS
    # -----------------------------------------

    with st.spinner("Loading filter options..."):
        metrics = get_dashboard_metrics()

    # -----------------------------------------
    # SIDEBAR
    # -----------------------------------------

    st.sidebar.markdown("### Filters")

    search_text = st.sidebar.text_input(
        "Search evidence",
        placeholder="Search review text..."
    )

    # Source
    sources = ["All"] + list(metrics["sources"].keys())

    selected_source = st.sidebar.selectbox(
        "Source",
        sources
    )

    # Evidence Type
    tiers = [
        "All Valid Evidence",
        "Direct Evidence",
        "Indirect Pre-Purchase",
        "Needs Validation",
        "Excluded"
    ]

    selected_tier = st.sidebar.selectbox(
        "Evidence Type",
        tiers
    )

    # Primary Barrier
    barriers = ["All"] + [
        format_label(x)
        for x in metrics["barriers"].keys()
    ]

    selected_barrier = st.sidebar.selectbox(
        "Primary Barrier",
        barriers
    )

    # Purchase Intent
    intents = ["All"] + [
        format_label(x)
        for x in metrics["intents"].keys()
    ]

    selected_intent = st.sidebar.selectbox(
        "Purchase Intent",
        intents
    )

    # Shopping Stage
    stages = ["All"] + [
        format_label(x)
        for x in metrics["stages"].keys()
    ]

    selected_stage = st.sidebar.selectbox(
        "Shopping Stage",
        stages
    )

    # -----------------------------------------
    # CONVERT UI LABELS BACK TO DATABASE VALUES
    # -----------------------------------------

    def reverse_enum_mapping(selected, available):

        if selected == "All":
            return "All"

        for raw_value in available:
            if format_label(raw_value) == selected:
                return raw_value

        return selected

    db_barrier = reverse_enum_mapping(
        selected_barrier,
        metrics["barriers"].keys()
    )

    db_intent = reverse_enum_mapping(
        selected_intent,
        metrics["intents"].keys()
    )

    db_stage = reverse_enum_mapping(
        selected_stage,
        metrics["stages"].keys()
    )

    # -----------------------------------------
    # FILTER PAYLOAD
    # -----------------------------------------

    filters = {
        "search_text": search_text,
        "source": selected_source,
        "tier": selected_tier,
        "barrier": db_barrier,
        "intent": db_intent,
        "stage": db_stage
    }

    # -----------------------------------------
    # FETCH DATA
    # -----------------------------------------

    with st.spinner("Fetching evidence..."):
        data = get_explorer_data(filters)

    # -----------------------------------------
    # RESULT COUNT
    # -----------------------------------------

    st.markdown(
        f"**Showing {len(data)} records matching the selected filters.**"
    )

    # -----------------------------------------
    # EMPTY STATE
    # -----------------------------------------

    if not data:
        st.info(
            "No records match all selected filters. "
            "Try removing one or more filters."
        )
        return

    # -----------------------------------------
    # EVIDENCE CARDS
    # -----------------------------------------

    for row in data:

        intent_label = format_label(
            row["purchase_intent"],
            "Unknown Intent"
        )

        barrier_label = format_label(
            row["primary_barrier"],
            "No Barrier"
        )

        evidence_type = row["direct_vs_indirect"]

        header = (
            f"[{row['source']}] "
            f"{intent_label} | "
            f"{barrier_label} "
            f"({evidence_type})"
        )

        with st.expander(header):

            # ---------------------------------
            # REVIEW TEXT
            # ---------------------------------

            st.markdown("### Review Text")

            review_text = str(row["text"]).strip()

            st.markdown(
                f"""
                <div style="
                    font-size: 16px;
                    font-weight: 500;
                    line-height: 1.6;
                    color: #111827;
                    padding: 12px 16px;
                    border-left: 4px solid #9ca3af;
                    background-color: #f9fafb;
                    border-radius: 4px;
                    margin-bottom: 18px;
                ">
                    {review_text}
                </div>
                """,
                unsafe_allow_html=True
            )

            # ---------------------------------
            # METADATA
            # ---------------------------------

            col1, col2 = st.columns(2)

            with col1:

                st.markdown(
                    f"**Source:** {row['source']}"
                )

                st.markdown(
                    f"**Timestamp:** {row['timestamp']}"
                )

                if row["url"]:
                    st.markdown(
                        f"[View Original Source]({row['url']})"
                    )

            with col2:

                st.markdown(
                    f"**Evidence Type:** {row['direct_vs_indirect']}"
                )

                st.markdown(
                    f"**AI Relevance:** {row['relevance']}"
                )

                st.markdown(
                    f"**Shopping Stage:** "
                    f"{format_label(row['shopping_stage'])}"
                )

                st.markdown(
                    f"**Secondary / Uncertainty:** "
                    f"{format_label(row['secondary_barrier'], 'None')}"
                )

                st.markdown(
                    f"**AI Confidence:** {row['ai_confidence']}"
                )