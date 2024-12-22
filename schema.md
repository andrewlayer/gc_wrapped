# Messages Database Schema

Generated on: 2024-12-22 14:10:10

## Table: _SqliteDatabaseProperties

### Columns

| Column | Type | NotNull | DefaultValue | PK |
|--------|------|----------|--------------|-----|
| key | TEXT | False |  | False |
| value | TEXT | False |  | False |

## Table: attachment

### Columns

| Column | Type | NotNull | DefaultValue | PK |
|--------|------|----------|--------------|-----|
| ROWID | INTEGER | False |  | True |
| guid | TEXT | True |  | False |
| created_date | INTEGER | False | 0 | False |
| start_date | INTEGER | False | 0 | False |
| filename | TEXT | False |  | False |
| uti | TEXT | False |  | False |
| mime_type | TEXT | False |  | False |
| transfer_state | INTEGER | False | 0 | False |
| is_outgoing | INTEGER | False | 0 | False |
| user_info | BLOB | False |  | False |
| transfer_name | TEXT | False |  | False |
| total_bytes | INTEGER | False | 0 | False |
| is_sticker | INTEGER | False | 0 | False |
| sticker_user_info | BLOB | False |  | False |
| attribution_info | BLOB | False |  | False |
| hide_attachment | INTEGER | False | 0 | False |
| ck_sync_state | INTEGER | False | 0 | False |
| ck_server_change_token_blob | BLOB | False |  | False |
| ck_record_id | TEXT | False |  | False |
| original_guid | TEXT | True |  | False |
| is_commsafety_sensitive | INTEGER | False | 0 | False |

### Indexes

```sql
CREATE INDEX attachment_idx_purged_attachments_v2 ON attachment(hide_attachment,ck_sync_state,transfer_state) WHERE hide_attachment=0 AND (ck_sync_state=1 OR ck_sync_state=4) AND transfer_state=0;
```

## Table: chat

### Columns

| Column | Type | NotNull | DefaultValue | PK |
|--------|------|----------|--------------|-----|
| ROWID | INTEGER | False |  | True |
| guid | TEXT | True |  | False |
| style | INTEGER | False |  | False |
| state | INTEGER | False |  | False |
| account_id | TEXT | False |  | False |
| properties | BLOB | False |  | False |
| chat_identifier | TEXT | False |  | False |
| service_name | TEXT | False |  | False |
| room_name | TEXT | False |  | False |
| account_login | TEXT | False |  | False |
| is_archived | INTEGER | False | 0 | False |
| last_addressed_handle | TEXT | False |  | False |
| display_name | TEXT | False |  | False |
| group_id | TEXT | False |  | False |
| is_filtered | INTEGER | False | 0 | False |
| successful_query | INTEGER | False |  | False |
| engram_id | TEXT | False |  | False |
| server_change_token | TEXT | False |  | False |
| ck_sync_state | INTEGER | False | 0 | False |
| original_group_id | TEXT | False |  | False |
| last_read_message_timestamp | INTEGER | False | 0 | False |
| cloudkit_record_id | TEXT | False |  | False |
| last_addressed_sim_id | TEXT | False |  | False |
| is_blackholed | INTEGER | False | 0 | False |
| syndication_date | INTEGER | False | 0 | False |
| syndication_type | INTEGER | False | 0 | False |
| is_recovered | INTEGER | False | 0 | False |
| is_deleting_incoming_messages | INTEGER | False | 0 | False |

### Indexes

```sql
CREATE INDEX chat_idx_chat_identifier_service_name ON chat(chat_identifier, service_name);
CREATE INDEX chat_idx_chat_identifier ON chat(chat_identifier);
CREATE INDEX chat_idx_chat_room_name_service_name ON chat(room_name, service_name);
CREATE INDEX chat_idx_is_archived ON chat(is_archived);
CREATE INDEX chat_idx_group_id ON chat(group_id);
```

## Table: chat_handle_join

### Columns

| Column | Type | NotNull | DefaultValue | PK |
|--------|------|----------|--------------|-----|
| chat_id | INTEGER | False |  | False |
| handle_id | INTEGER | False |  | False |

### Foreign Keys

| Column | References | On Delete | On Update |
|--------|------------|-----------|-----------|
| handle_id | handle(ROWID) | CASCADE | NO ACTION |
| chat_id | chat(ROWID) | CASCADE | NO ACTION |

### Indexes

```sql
CREATE INDEX chat_handle_join_idx_handle_id ON chat_handle_join(handle_id);
```

## Table: chat_message_join

### Columns

| Column | Type | NotNull | DefaultValue | PK |
|--------|------|----------|--------------|-----|
| chat_id | INTEGER | False |  | True |
| message_id | INTEGER | False |  | True |
| message_date | INTEGER | False | 0 | False |

### Foreign Keys

| Column | References | On Delete | On Update |
|--------|------------|-----------|-----------|
| message_id | message(ROWID) | CASCADE | NO ACTION |
| chat_id | chat(ROWID) | CASCADE | NO ACTION |

### Indexes

```sql
CREATE INDEX chat_message_join_idx_message_id_only ON chat_message_join(message_id);
CREATE INDEX chat_message_join_idx_chat_id ON chat_message_join(chat_id);
CREATE INDEX chat_message_join_idx_message_date_id_chat_id ON chat_message_join(chat_id, message_date, message_id);
```

## Table: chat_recoverable_message_join

### Columns

| Column | Type | NotNull | DefaultValue | PK |
|--------|------|----------|--------------|-----|
| chat_id | INTEGER | False |  | True |
| message_id | INTEGER | False |  | True |
| delete_date | INTEGER | False |  | False |
| ck_sync_state | INTEGER | False | 0 | False |

### Foreign Keys

| Column | References | On Delete | On Update |
|--------|------------|-----------|-----------|
| message_id | message(ROWID) | CASCADE | NO ACTION |
| chat_id | chat(ROWID) | CASCADE | NO ACTION |

## Table: deleted_messages

### Columns

| Column | Type | NotNull | DefaultValue | PK |
|--------|------|----------|--------------|-----|
| ROWID | INTEGER | False |  | True |
| guid | TEXT | True |  | False |

## Table: handle

### Columns

| Column | Type | NotNull | DefaultValue | PK |
|--------|------|----------|--------------|-----|
| ROWID | INTEGER | False |  | True |
| id | TEXT | True |  | False |
| country | TEXT | False |  | False |
| service | TEXT | True |  | False |
| uncanonicalized_id | TEXT | False |  | False |
| person_centric_id | TEXT | False |  | False |

## Table: kvtable

### Columns

| Column | Type | NotNull | DefaultValue | PK |
|--------|------|----------|--------------|-----|
| ROWID | INTEGER | False |  | True |
| key | TEXT | True |  | False |
| value | BLOB | True |  | False |

## Table: message

### Columns

| Column | Type | NotNull | DefaultValue | PK |
|--------|------|----------|--------------|-----|
| ROWID | INTEGER | False |  | True |
| guid | TEXT | True |  | False |
| text | TEXT | False |  | False |
| replace | INTEGER | False | 0 | False |
| service_center | TEXT | False |  | False |
| handle_id | INTEGER | False | 0 | False |
| subject | TEXT | False |  | False |
| country | TEXT | False |  | False |
| attributedBody | BLOB | False |  | False |
| version | INTEGER | False | 0 | False |
| type | INTEGER | False | 0 | False |
| service | TEXT | False |  | False |
| account | TEXT | False |  | False |
| account_guid | TEXT | False |  | False |
| error | INTEGER | False | 0 | False |
| date | INTEGER | False |  | False |
| date_read | INTEGER | False |  | False |
| date_delivered | INTEGER | False |  | False |
| is_delivered | INTEGER | False | 0 | False |
| is_finished | INTEGER | False | 0 | False |
| is_emote | INTEGER | False | 0 | False |
| is_from_me | INTEGER | False | 0 | False |
| is_empty | INTEGER | False | 0 | False |
| is_delayed | INTEGER | False | 0 | False |
| is_auto_reply | INTEGER | False | 0 | False |
| is_prepared | INTEGER | False | 0 | False |
| is_read | INTEGER | False | 0 | False |
| is_system_message | INTEGER | False | 0 | False |
| is_sent | INTEGER | False | 0 | False |
| has_dd_results | INTEGER | False | 0 | False |
| is_service_message | INTEGER | False | 0 | False |
| is_forward | INTEGER | False | 0 | False |
| was_downgraded | INTEGER | False | 0 | False |
| is_archive | INTEGER | False | 0 | False |
| cache_has_attachments | INTEGER | False | 0 | False |
| cache_roomnames | TEXT | False |  | False |
| was_data_detected | INTEGER | False | 0 | False |
| was_deduplicated | INTEGER | False | 0 | False |
| is_audio_message | INTEGER | False | 0 | False |
| is_played | INTEGER | False | 0 | False |
| date_played | INTEGER | False |  | False |
| item_type | INTEGER | False | 0 | False |
| other_handle | INTEGER | False | 0 | False |
| group_title | TEXT | False |  | False |
| group_action_type | INTEGER | False | 0 | False |
| share_status | INTEGER | False | 0 | False |
| share_direction | INTEGER | False | 0 | False |
| is_expirable | INTEGER | False | 0 | False |
| expire_state | INTEGER | False | 0 | False |
| message_action_type | INTEGER | False | 0 | False |
| message_source | INTEGER | False | 0 | False |
| associated_message_guid | TEXT | False |  | False |
| associated_message_type | INTEGER | False | 0 | False |
| balloon_bundle_id | TEXT | False |  | False |
| payload_data | BLOB | False |  | False |
| expressive_send_style_id | TEXT | False |  | False |
| associated_message_range_location | INTEGER | False | 0 | False |
| associated_message_range_length | INTEGER | False | 0 | False |
| time_expressive_send_played | INTEGER | False |  | False |
| message_summary_info | BLOB | False |  | False |
| ck_sync_state | INTEGER | False | 0 | False |
| ck_record_id | TEXT | False |  | False |
| ck_record_change_tag | TEXT | False |  | False |
| destination_caller_id | TEXT | False |  | False |
| is_corrupt | INTEGER | False | 0 | False |
| reply_to_guid | TEXT | False |  | False |
| sort_id | INTEGER | False |  | False |
| is_spam | INTEGER | False | 0 | False |
| has_unseen_mention | INTEGER | False | 0 | False |
| thread_originator_guid | TEXT | False |  | False |
| thread_originator_part | TEXT | False |  | False |
| syndication_ranges | TEXT | False |  | False |
| synced_syndication_ranges | TEXT | False |  | False |
| was_delivered_quietly | INTEGER | False | 0 | False |
| did_notify_recipient | INTEGER | False | 0 | False |
| date_retracted | INTEGER | False | 0 | False |
| date_edited | INTEGER | False | 0 | False |
| was_detonated | INTEGER | False | 0 | False |
| part_count | INTEGER | False |  | False |
| is_stewie | INTEGER | False | 0 | False |
| is_kt_verified | INTEGER | False | 0 | False |
| is_sos | INTEGER | False | 0 | False |
| is_critical | INTEGER | False | 0 | False |
| bia_reference_id | TEXT | False | NULL | False |
| fallback_hash | TEXT | False | NULL | False |

### Indexes

```sql
CREATE INDEX message_idx_date ON message(date);
CREATE INDEX message_idx_thread_originator_guid ON message(thread_originator_guid);
CREATE INDEX message_idx_handle ON message(handle_id, date);
CREATE INDEX message_idx_handle_id ON message(handle_id);
CREATE INDEX message_idx_is_sent_is_from_me_error ON message(is_sent, is_from_me, error);
CREATE INDEX message_idx_associated_message ON message(associated_message_guid);
CREATE INDEX message_idx_undelivered_one_to_one_imessage ON message(cache_roomnames,service,is_sent,is_delivered,was_downgraded,item_type) where cache_roomnames IS NULL AND service = 'iMessage' AND is_sent = 1 AND is_delivered = 0 AND was_downgraded = 0 AND item_type == 0;
CREATE INDEX message_idx_cache_has_attachments ON message(cache_has_attachments);
CREATE INDEX message_idx_other_handle ON message(other_handle);
CREATE INDEX message_idx_was_downgraded ON message(was_downgraded);
CREATE INDEX message_idx_expire_state ON message(expire_state);
CREATE INDEX message_idx_is_read ON message(is_read, is_from_me, is_finished);
CREATE INDEX message_idx_isRead_isFromMe_itemType ON message(is_read, is_from_me, item_type);
CREATE INDEX message_idx_failed ON message(is_finished, is_from_me, error);
```

## Table: message_attachment_join

### Columns

| Column | Type | NotNull | DefaultValue | PK |
|--------|------|----------|--------------|-----|
| message_id | INTEGER | False |  | False |
| attachment_id | INTEGER | False |  | False |

### Foreign Keys

| Column | References | On Delete | On Update |
|--------|------------|-----------|-----------|
| attachment_id | attachment(ROWID) | CASCADE | NO ACTION |
| message_id | message(ROWID) | CASCADE | NO ACTION |

### Indexes

```sql
CREATE INDEX message_attachment_join_idx_message_id ON message_attachment_join(message_id);
CREATE INDEX message_attachment_join_idx_attachment_id ON message_attachment_join(attachment_id);
```

## Table: message_processing_task

### Columns

| Column | Type | NotNull | DefaultValue | PK |
|--------|------|----------|--------------|-----|
| ROWID | INTEGER | False |  | True |
| guid | TEXT | True |  | False |
| task_flags | INTEGER | True |  | False |

### Indexes

```sql
CREATE INDEX message_processing_task_idx_guid_task_flags ON message_processing_task(guid, task_flags);
```

## Table: recoverable_message_part

### Columns

| Column | Type | NotNull | DefaultValue | PK |
|--------|------|----------|--------------|-----|
| chat_id | INTEGER | False |  | True |
| message_id | INTEGER | False |  | True |
| part_index | INTEGER | False |  | True |
| delete_date | INTEGER | False |  | False |
| part_text | BLOB | True |  | False |
| ck_sync_state | INTEGER | False | 0 | False |

### Foreign Keys

| Column | References | On Delete | On Update |
|--------|------------|-----------|-----------|
| message_id | message(ROWID) | CASCADE | NO ACTION |
| chat_id | chat(ROWID) | CASCADE | NO ACTION |

## Table: sync_deleted_attachments

### Columns

| Column | Type | NotNull | DefaultValue | PK |
|--------|------|----------|--------------|-----|
| ROWID | INTEGER | False |  | True |
| guid | TEXT | True |  | False |
| recordID | TEXT | False |  | False |

## Table: sync_deleted_chats

### Columns

| Column | Type | NotNull | DefaultValue | PK |
|--------|------|----------|--------------|-----|
| ROWID | INTEGER | False |  | True |
| guid | TEXT | True |  | False |
| recordID | TEXT | False |  | False |
| timestamp | INTEGER | False |  | False |

## Table: sync_deleted_messages

### Columns

| Column | Type | NotNull | DefaultValue | PK |
|--------|------|----------|--------------|-----|
| ROWID | INTEGER | False |  | True |
| guid | TEXT | True |  | False |
| recordID | TEXT | False |  | False |

## Table: unsynced_removed_recoverable_messages

### Columns

| Column | Type | NotNull | DefaultValue | PK |
|--------|------|----------|--------------|-----|
| ROWID | INTEGER | False |  | True |
| chat_guid | TEXT | True |  | False |
| message_guid | TEXT | True |  | False |
| part_index | INTEGER | False |  | False |
