import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.models.sources import Source
from app.models.collection_runs import CollectionRun
from app.models.conversations import Conversation
from app.models.analyses import Analysis
from app.models.insights import Insight

@pytest.mark.asyncio
async def test_create_source(db_session: AsyncSession):
    source = Source(platform="youtube", name="YouTube", base_url="https://youtube.com")
    db_session.add(source)
    await db_session.commit()
    assert source.id is not None
    assert source.platform == "youtube"

@pytest.mark.asyncio
async def test_duplicate_external_id_constraint(db_session: AsyncSession):
    source = Source(platform="play_store", name="Google Play")
    db_session.add(source)
    await db_session.commit()

    conv1 = Conversation(
        source_id=source.id,
        external_id="duplicate-123",
        raw_content="First",
        author="user1"
    )
    db_session.add(conv1)
    await db_session.commit()

    conv2 = Conversation(
        source_id=source.id,
        external_id="duplicate-123",
        raw_content="Second",
        author="user2"
    )
    db_session.add(conv2)
    
    with pytest.raises(IntegrityError):
        await db_session.commit()
    
    await db_session.rollback()

@pytest.mark.asyncio
async def test_full_relationship_chain(db_session: AsyncSession):
    # 1. Source
    source = Source(platform="app_store", name="App Store")
    db_session.add(source)
    await db_session.flush()

    # 2. Run
    run = CollectionRun(source_id=source.id, status="completed")
    db_session.add(run)
    await db_session.flush()

    # 3. Conversation
    conv = Conversation(
        source_id=source.id,
        collection_run_id=run.id,
        external_id="ext-unique-456",
        raw_content="Need more colors",
        author="user1"
    )
    db_session.add(conv)
    await db_session.flush()

    # 4. Analysis
    analysis = Analysis(
        conversation_id=conv.id,
        relevance="high",
        primary_barrier="color_options",
        secondary_barriers=["availability", "price"],
        product_category="shoes",
        confidence=0.95
    )
    db_session.add(analysis)
    await db_session.flush()

    # 5. Insight
    insight = Insight(
        title="Users want more colors in shoes",
        description="High demand for missing colors",
        evidence_count=1,
        confidence_score=0.95
    )
    db_session.add(insight)
    
    await db_session.commit()

    # Verify chain
    assert analysis.id is not None
    assert "availability" in analysis.secondary_barriers
    assert analysis.conversation.id == conv.id
    assert analysis.conversation.source.id == source.id
    assert insight.id is not None
    assert insight.title == "Users want more colors in shoes"
