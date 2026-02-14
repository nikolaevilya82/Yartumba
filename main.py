id: Mapped[uuid.UUID] = mapped_column(
    UUID(as_uuid=True),
    primary_key=True,
    default=uuid.uuid4
)
client_id: Mapped[uuid.UUID] = mapped_column(
    ForeignKey("client.id", ondelete="CASCADE"),
    nullable=False
)