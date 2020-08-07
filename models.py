# coding: utf-8
from sqlalchemy import CHAR, Column, DECIMAL, DateTime, Float, ForeignKey, Index, String, TIMESTAMP, Text, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, LONGTEXT, MEDIUMTEXT, SMALLINT, TINYINT, TINYTEXT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class WpActionschedulerAction(Base):
    __tablename__ = 'wp_actionscheduler_actions'

    action_id = Column(BIGINT(20), primary_key=True)
    hook = Column(String(191, 'utf8mb4_unicode_520_ci'), nullable=False, index=True)
    status = Column(String(20, 'utf8mb4_unicode_520_ci'), nullable=False, index=True)
    scheduled_date_gmt = Column(DateTime, nullable=False, index=True, server_default=text("'0000-00-00 00:00:00'"))
    scheduled_date_local = Column(DateTime, nullable=False, server_default=text("'0000-00-00 00:00:00'"))
    args = Column(String(191, 'utf8mb4_unicode_520_ci'), index=True)
    schedule = Column(LONGTEXT)
    group_id = Column(BIGINT(20), nullable=False, index=True, server_default=text("'0'"))
    attempts = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    last_attempt_gmt = Column(DateTime, nullable=False, index=True, server_default=text("'0000-00-00 00:00:00'"))
    last_attempt_local = Column(DateTime, nullable=False, server_default=text("'0000-00-00 00:00:00'"))
    claim_id = Column(BIGINT(20), nullable=False, index=True, server_default=text("'0'"))
    extended_args = Column(String(8000, 'utf8mb4_unicode_520_ci'))


class WpActionschedulerClaim(Base):
    __tablename__ = 'wp_actionscheduler_claims'

    claim_id = Column(BIGINT(20), primary_key=True)
    date_created_gmt = Column(DateTime, nullable=False, index=True, server_default=text("'0000-00-00 00:00:00'"))


class WpActionschedulerGroup(Base):
    __tablename__ = 'wp_actionscheduler_groups'

    group_id = Column(BIGINT(20), primary_key=True)
    slug = Column(String(255, 'utf8mb4_unicode_520_ci'), nullable=False, index=True)


class WpActionschedulerLog(Base):
    __tablename__ = 'wp_actionscheduler_logs'

    log_id = Column(BIGINT(20), primary_key=True)
    action_id = Column(BIGINT(20), nullable=False, index=True)
    message = Column(Text(collation='utf8mb4_unicode_520_ci'), nullable=False)
    log_date_gmt = Column(DateTime, nullable=False, index=True, server_default=text("'0000-00-00 00:00:00'"))
    log_date_local = Column(DateTime, nullable=False, server_default=text("'0000-00-00 00:00:00'"))


class WpCommentmeta(Base):
    __tablename__ = 'wp_commentmeta'

    meta_id = Column(BIGINT(20), primary_key=True)
    comment_id = Column(BIGINT(20), nullable=False, index=True, server_default=text("'0'"))
    meta_key = Column(String(255, 'utf8mb4_unicode_ci'), index=True)
    meta_value = Column(LONGTEXT)


class WpComment(Base):
    __tablename__ = 'wp_comments'
    __table_args__ = (
        Index('comment_approved_date_gmt', 'comment_approved', 'comment_date_gmt'),
    )

    comment_ID = Column(BIGINT(20), primary_key=True)
    comment_post_ID = Column(BIGINT(20), nullable=False, index=True, server_default=text("'0'"))
    comment_author = Column(TINYTEXT, nullable=False)
    comment_author_email = Column(String(100, 'utf8mb4_unicode_ci'), nullable=False, index=True, server_default=text("''"))
    comment_author_url = Column(String(200, 'utf8mb4_unicode_ci'), nullable=False, server_default=text("''"))
    comment_author_IP = Column(String(100, 'utf8mb4_unicode_ci'), nullable=False, server_default=text("''"))
    comment_date = Column(DateTime, nullable=False, server_default=text("'0000-00-00 00:00:00'"))
    comment_date_gmt = Column(DateTime, nullable=False, index=True, server_default=text("'0000-00-00 00:00:00'"))
    comment_content = Column(Text(collation='utf8mb4_unicode_ci'), nullable=False)
    comment_karma = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    comment_approved = Column(String(20, 'utf8mb4_unicode_ci'), nullable=False, server_default=text("'1'"))
    comment_agent = Column(String(255, 'utf8mb4_unicode_ci'), nullable=False, server_default=text("''"))
    comment_type = Column(String(20, 'utf8mb4_unicode_ci'), nullable=False, index=True, server_default=text("''"))
    comment_parent = Column(BIGINT(20), nullable=False, index=True, server_default=text("'0'"))
    user_id = Column(BIGINT(20), nullable=False, server_default=text("'0'"))


class WpLink(Base):
    __tablename__ = 'wp_links'

    link_id = Column(BIGINT(20), primary_key=True)
    link_url = Column(String(255, 'utf8mb4_unicode_ci'), nullable=False, server_default=text("''"))
    link_name = Column(String(255, 'utf8mb4_unicode_ci'), nullable=False, server_default=text("''"))
    link_image = Column(String(255, 'utf8mb4_unicode_ci'), nullable=False, server_default=text("''"))
    link_target = Column(String(25, 'utf8mb4_unicode_ci'), nullable=False, server_default=text("''"))
    link_description = Column(String(255, 'utf8mb4_unicode_ci'), nullable=False, server_default=text("''"))
    link_visible = Column(String(20, 'utf8mb4_unicode_ci'), nullable=False, index=True, server_default=text("'Y'"))
    link_owner = Column(BIGINT(20), nullable=False, server_default=text("'1'"))
    link_rating = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    link_updated = Column(DateTime, nullable=False, server_default=text("'0000-00-00 00:00:00'"))
    link_rel = Column(String(255, 'utf8mb4_unicode_ci'), nullable=False, server_default=text("''"))
    link_notes = Column(MEDIUMTEXT, nullable=False)
    link_rss = Column(String(255, 'utf8mb4_unicode_ci'), nullable=False, server_default=text("''"))


class WpOption(Base):
    __tablename__ = 'wp_options'

    option_id = Column(BIGINT(20), primary_key=True)
    option_name = Column(String(191, 'utf8mb4_unicode_ci'), nullable=False, unique=True, server_default=text("''"))
    option_value = Column(LONGTEXT, nullable=False)
    autoload = Column(String(20, 'utf8mb4_unicode_ci'), nullable=False, index=True, server_default=text("'yes'"))


class WpPostmeta(Base):
    __tablename__ = 'wp_postmeta'

    meta_id = Column(BIGINT(20), primary_key=True)
    post_id = Column(BIGINT(20), nullable=False, index=True, server_default=text("'0'"))
    meta_key = Column(String(255, 'utf8mb4_unicode_ci'), index=True)
    meta_value = Column(LONGTEXT)


class WpPost(Base):
    __tablename__ = 'wp_posts'
    __table_args__ = (
        Index('type_status_date', 'post_type', 'post_status', 'post_date', 'ID'),
    )

    ID = Column(BIGINT(20), primary_key=True)
    post_author = Column(BIGINT(20), nullable=False, index=True, server_default=text("'0'"))
    post_date = Column(DateTime, nullable=False, server_default=text("'0000-00-00 00:00:00'"))
    post_date_gmt = Column(DateTime, nullable=False, server_default=text("'0000-00-00 00:00:00'"))
    post_content = Column(LONGTEXT, nullable=False)
    post_title = Column(Text(collation='utf8mb4_unicode_ci'), nullable=False)
    post_excerpt = Column(Text(collation='utf8mb4_unicode_ci'), nullable=False)
    post_status = Column(String(20, 'utf8mb4_unicode_ci'), nullable=False, server_default=text("'publish'"))
    comment_status = Column(String(20, 'utf8mb4_unicode_ci'), nullable=False, server_default=text("'open'"))
    ping_status = Column(String(20, 'utf8mb4_unicode_ci'), nullable=False, server_default=text("'open'"))
    post_password = Column(String(255, 'utf8mb4_unicode_ci'), nullable=False, server_default=text("''"))
    post_name = Column(String(200, 'utf8mb4_unicode_ci'), nullable=False, index=True, server_default=text("''"))
    to_ping = Column(Text(collation='utf8mb4_unicode_ci'), nullable=False)
    pinged = Column(Text(collation='utf8mb4_unicode_ci'), nullable=False)
    post_modified = Column(DateTime, nullable=False, server_default=text("'0000-00-00 00:00:00'"))
    post_modified_gmt = Column(DateTime, nullable=False, server_default=text("'0000-00-00 00:00:00'"))
    post_content_filtered = Column(LONGTEXT, nullable=False)
    post_parent = Column(BIGINT(20), nullable=False, index=True, server_default=text("'0'"))
    guid = Column(String(255, 'utf8mb4_unicode_ci'), nullable=False, server_default=text("''"))
    menu_order = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    post_type = Column(String(20, 'utf8mb4_unicode_ci'), nullable=False, server_default=text("'post'"))
    post_mime_type = Column(String(100, 'utf8mb4_unicode_ci'), nullable=False, server_default=text("''"))
    comment_count = Column(BIGINT(20), nullable=False, server_default=text("'0'"))


class WpTermRelationship(Base):
    __tablename__ = 'wp_term_relationships'

    object_id = Column(BIGINT(20), primary_key=True, nullable=False, server_default=text("'0'"))
    term_taxonomy_id = Column(BIGINT(20), primary_key=True, nullable=False, index=True, server_default=text("'0'"))
    term_order = Column(INTEGER(11), nullable=False, server_default=text("'0'"))


class WpTermTaxonomy(Base):
    __tablename__ = 'wp_term_taxonomy'
    __table_args__ = (
        Index('term_id_taxonomy', 'term_id', 'taxonomy', unique=True),
    )

    term_taxonomy_id = Column(BIGINT(20), primary_key=True)
    term_id = Column(BIGINT(20), nullable=False, server_default=text("'0'"))
    taxonomy = Column(String(32, 'utf8mb4_unicode_ci'), nullable=False, index=True, server_default=text("''"))
    description = Column(LONGTEXT, nullable=False)
    parent = Column(BIGINT(20), nullable=False, server_default=text("'0'"))
    count = Column(BIGINT(20), nullable=False, server_default=text("'0'"))


class WpTermmeta(Base):
    __tablename__ = 'wp_termmeta'

    meta_id = Column(BIGINT(20), primary_key=True)
    term_id = Column(BIGINT(20), nullable=False, index=True, server_default=text("'0'"))
    meta_key = Column(String(255, 'utf8mb4_unicode_ci'), index=True)
    meta_value = Column(LONGTEXT)


class WpTerm(Base):
    __tablename__ = 'wp_terms'

    term_id = Column(BIGINT(20), primary_key=True)
    name = Column(String(200, 'utf8mb4_unicode_ci'), nullable=False, index=True, server_default=text("''"))
    slug = Column(String(200, 'utf8mb4_unicode_ci'), nullable=False, index=True, server_default=text("''"))
    term_group = Column(BIGINT(10), nullable=False, server_default=text("'0'"))


class WpUsermeta(Base):
    __tablename__ = 'wp_usermeta'

    umeta_id = Column(BIGINT(20), primary_key=True)
    user_id = Column(BIGINT(20), nullable=False, index=True, server_default=text("'0'"))
    meta_key = Column(String(255, 'utf8mb4_unicode_ci'), index=True)
    meta_value = Column(LONGTEXT)


class WpUser(Base):
    __tablename__ = 'wp_users'

    ID = Column(BIGINT(20), primary_key=True)
    user_login = Column(String(60, 'utf8mb4_unicode_ci'), nullable=False, index=True, server_default=text("''"))
    user_pass = Column(String(255, 'utf8mb4_unicode_ci'), nullable=False, server_default=text("''"))
    user_nicename = Column(String(50, 'utf8mb4_unicode_ci'), nullable=False, index=True, server_default=text("''"))
    user_email = Column(String(100, 'utf8mb4_unicode_ci'), nullable=False, index=True, server_default=text("''"))
    user_url = Column(String(100, 'utf8mb4_unicode_ci'), nullable=False, server_default=text("''"))
    user_registered = Column(DateTime, nullable=False, server_default=text("'0000-00-00 00:00:00'"))
    user_activation_key = Column(String(255, 'utf8mb4_unicode_ci'), nullable=False, server_default=text("''"))
    user_status = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    display_name = Column(String(250, 'utf8mb4_unicode_ci'), nullable=False, server_default=text("''"))


class WpWcAdminNoteAction(Base):
    __tablename__ = 'wp_wc_admin_note_actions'

    action_id = Column(BIGINT(20), primary_key=True)
    note_id = Column(BIGINT(20), nullable=False, index=True)
    name = Column(String(255, 'utf8mb4_unicode_520_ci'), nullable=False)
    label = Column(String(255, 'utf8mb4_unicode_520_ci'), nullable=False)
    query = Column(LONGTEXT, nullable=False)
    status = Column(String(255, 'utf8mb4_unicode_520_ci'), nullable=False)
    is_primary = Column(TINYINT(1), nullable=False, server_default=text("'0'"))


class WpWcAdminNote(Base):
    __tablename__ = 'wp_wc_admin_notes'

    note_id = Column(BIGINT(20), primary_key=True)
    name = Column(String(255, 'utf8mb4_unicode_520_ci'), nullable=False)
    type = Column(String(20, 'utf8mb4_unicode_520_ci'), nullable=False)
    locale = Column(String(20, 'utf8mb4_unicode_520_ci'), nullable=False)
    title = Column(LONGTEXT, nullable=False)
    content = Column(LONGTEXT, nullable=False)
    content_data = Column(LONGTEXT)
    status = Column(String(200, 'utf8mb4_unicode_520_ci'), nullable=False)
    source = Column(String(200, 'utf8mb4_unicode_520_ci'), nullable=False)
    date_created = Column(DateTime, nullable=False, server_default=text("'0000-00-00 00:00:00'"))
    date_reminder = Column(DateTime)
    is_snoozable = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
    layout = Column(String(20, 'utf8mb4_unicode_520_ci'), nullable=False, server_default=text("''"))
    image = Column(String(200, 'utf8mb4_unicode_520_ci'))
    is_deleted = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
    icon = Column(String(200, 'utf8mb4_unicode_520_ci'), nullable=False, server_default=text("'info'"))


class WpWcCategoryLookup(Base):
    __tablename__ = 'wp_wc_category_lookup'

    category_tree_id = Column(BIGINT(20), primary_key=True, nullable=False)
    category_id = Column(BIGINT(20), primary_key=True, nullable=False)


class WpWcCustomerLookup(Base):
    __tablename__ = 'wp_wc_customer_lookup'

    customer_id = Column(BIGINT(20), primary_key=True)
    user_id = Column(BIGINT(20), unique=True)
    username = Column(String(60, 'utf8mb4_unicode_520_ci'), nullable=False, server_default=text("''"))
    first_name = Column(String(255, 'utf8mb4_unicode_520_ci'), nullable=False)
    last_name = Column(String(255, 'utf8mb4_unicode_520_ci'), nullable=False)
    email = Column(String(100, 'utf8mb4_unicode_520_ci'), index=True)
    date_last_active = Column(TIMESTAMP)
    date_registered = Column(TIMESTAMP)
    country = Column(CHAR(2, 'utf8mb4_unicode_520_ci'), nullable=False, server_default=text("''"))
    postcode = Column(String(20, 'utf8mb4_unicode_520_ci'), nullable=False, server_default=text("''"))
    city = Column(String(100, 'utf8mb4_unicode_520_ci'), nullable=False, server_default=text("''"))
    state = Column(String(100, 'utf8mb4_unicode_520_ci'), nullable=False, server_default=text("''"))


class WpWcOrderCouponLookup(Base):
    __tablename__ = 'wp_wc_order_coupon_lookup'

    order_id = Column(BIGINT(20), primary_key=True, nullable=False)
    coupon_id = Column(BIGINT(20), primary_key=True, nullable=False, index=True)
    date_created = Column(DateTime, nullable=False, index=True, server_default=text("'0000-00-00 00:00:00'"))
    discount_amount = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))


class WpWcOrderProductLookup(Base):
    __tablename__ = 'wp_wc_order_product_lookup'

    order_item_id = Column(BIGINT(20), primary_key=True)
    order_id = Column(BIGINT(20), nullable=False, index=True)
    product_id = Column(BIGINT(20), nullable=False, index=True)
    variation_id = Column(BIGINT(20), nullable=False)
    customer_id = Column(BIGINT(20), index=True)
    date_created = Column(DateTime, nullable=False, index=True, server_default=text("'0000-00-00 00:00:00'"))
    product_qty = Column(INTEGER(11), nullable=False)
    product_net_revenue = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    product_gross_revenue = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    coupon_amount = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    tax_amount = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    shipping_amount = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    shipping_tax_amount = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))


class WpWcOrderStat(Base):
    __tablename__ = 'wp_wc_order_stats'

    order_id = Column(BIGINT(20), primary_key=True)
    parent_id = Column(BIGINT(20), nullable=False, server_default=text("'0'"))
    date_created = Column(DateTime, nullable=False, index=True, server_default=text("'0000-00-00 00:00:00'"))
    date_created_gmt = Column(DateTime, nullable=False, server_default=text("'0000-00-00 00:00:00'"))
    num_items_sold = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    total_sales = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    tax_total = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    shipping_total = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    net_total = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    returning_customer = Column(TINYINT(1))
    status = Column(String(200, 'utf8mb4_unicode_520_ci'), nullable=False, index=True)
    customer_id = Column(BIGINT(20), nullable=False, index=True)


class WpWcOrderTaxLookup(Base):
    __tablename__ = 'wp_wc_order_tax_lookup'

    order_id = Column(BIGINT(20), primary_key=True, nullable=False)
    tax_rate_id = Column(BIGINT(20), primary_key=True, nullable=False, index=True)
    date_created = Column(DateTime, nullable=False, index=True, server_default=text("'0000-00-00 00:00:00'"))
    shipping_tax = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    order_tax = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    total_tax = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))


class WpWcProductMetaLookup(Base):
    __tablename__ = 'wp_wc_product_meta_lookup'
    __table_args__ = (
        Index('min_max_price', 'min_price', 'max_price'),
    )

    product_id = Column(BIGINT(20), primary_key=True)
    sku = Column(String(100, 'utf8mb4_unicode_520_ci'), server_default=text("''"))
    virtual = Column(TINYINT(1), index=True, server_default=text("'0'"))
    downloadable = Column(TINYINT(1), index=True, server_default=text("'0'"))
    min_price = Column(DECIMAL(19, 4))
    max_price = Column(DECIMAL(19, 4))
    onsale = Column(TINYINT(1), index=True, server_default=text("'0'"))
    stock_quantity = Column(Float(asdecimal=True), index=True)
    stock_status = Column(String(100, 'utf8mb4_unicode_520_ci'), index=True, server_default=text("'instock'"))
    rating_count = Column(BIGINT(20), server_default=text("'0'"))
    average_rating = Column(DECIMAL(3, 2), server_default=text("'0.00'"))
    total_sales = Column(BIGINT(20), server_default=text("'0'"))
    tax_status = Column(String(100, 'utf8mb4_unicode_520_ci'), server_default=text("'taxable'"))
    tax_class = Column(String(100, 'utf8mb4_unicode_520_ci'), server_default=text("''"))


class WpWcReservedStock(Base):
    __tablename__ = 'wp_wc_reserved_stock'

    order_id = Column(BIGINT(20), primary_key=True, nullable=False)
    product_id = Column(BIGINT(20), primary_key=True, nullable=False)
    stock_quantity = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    timestamp = Column(DateTime, nullable=False, server_default=text("'0000-00-00 00:00:00'"))
    expires = Column(DateTime, nullable=False, server_default=text("'0000-00-00 00:00:00'"))


class WpWcTaxRateClass(Base):
    __tablename__ = 'wp_wc_tax_rate_classes'

    tax_rate_class_id = Column(BIGINT(20), primary_key=True)
    name = Column(String(200, 'utf8mb4_unicode_520_ci'), nullable=False, server_default=text("''"))
    slug = Column(String(200, 'utf8mb4_unicode_520_ci'), nullable=False, unique=True, server_default=text("''"))


class WpWcWebhook(Base):
    __tablename__ = 'wp_wc_webhooks'

    webhook_id = Column(BIGINT(20), primary_key=True)
    status = Column(String(200, 'utf8mb4_unicode_520_ci'), nullable=False)
    name = Column(Text(collation='utf8mb4_unicode_520_ci'), nullable=False)
    user_id = Column(BIGINT(20), nullable=False, index=True)
    delivery_url = Column(Text(collation='utf8mb4_unicode_520_ci'), nullable=False)
    secret = Column(Text(collation='utf8mb4_unicode_520_ci'), nullable=False)
    topic = Column(String(200, 'utf8mb4_unicode_520_ci'), nullable=False)
    date_created = Column(DateTime, nullable=False, server_default=text("'0000-00-00 00:00:00'"))
    date_created_gmt = Column(DateTime, nullable=False, server_default=text("'0000-00-00 00:00:00'"))
    date_modified = Column(DateTime, nullable=False, server_default=text("'0000-00-00 00:00:00'"))
    date_modified_gmt = Column(DateTime, nullable=False, server_default=text("'0000-00-00 00:00:00'"))
    api_version = Column(SMALLINT(4), nullable=False)
    failure_count = Column(SMALLINT(10), nullable=False, server_default=text("'0'"))
    pending_delivery = Column(TINYINT(1), nullable=False, server_default=text("'0'"))


class WpWoocommerceApiKey(Base):
    __tablename__ = 'wp_woocommerce_api_keys'

    key_id = Column(BIGINT(20), primary_key=True)
    user_id = Column(BIGINT(20), nullable=False)
    description = Column(String(200, 'utf8mb4_unicode_520_ci'))
    permissions = Column(String(10, 'utf8mb4_unicode_520_ci'), nullable=False)
    consumer_key = Column(CHAR(64, 'utf8mb4_unicode_520_ci'), nullable=False, index=True)
    consumer_secret = Column(CHAR(43, 'utf8mb4_unicode_520_ci'), nullable=False, index=True)
    nonces = Column(LONGTEXT)
    truncated_key = Column(CHAR(7, 'utf8mb4_unicode_520_ci'), nullable=False)
    last_access = Column(DateTime)


class WpWoocommerceAttributeTaxonomy(Base):
    __tablename__ = 'wp_woocommerce_attribute_taxonomies'

    attribute_id = Column(BIGINT(20), primary_key=True)
    attribute_name = Column(String(200, 'utf8mb4_unicode_520_ci'), nullable=False, index=True)
    attribute_label = Column(String(200, 'utf8mb4_unicode_520_ci'))
    attribute_type = Column(String(20, 'utf8mb4_unicode_520_ci'), nullable=False)
    attribute_orderby = Column(String(20, 'utf8mb4_unicode_520_ci'), nullable=False)
    attribute_public = Column(INTEGER(1), nullable=False, server_default=text("'1'"))


class WpWoocommerceDownloadableProductPermission(Base):
    __tablename__ = 'wp_woocommerce_downloadable_product_permissions'
    __table_args__ = (
        Index('download_order_product', 'download_id', 'order_id', 'product_id'),
        Index('download_order_key_product', 'product_id', 'order_id', 'order_key', 'download_id'),
        Index('user_order_remaining_expires', 'user_id', 'order_id', 'downloads_remaining', 'access_expires')
    )

    permission_id = Column(BIGINT(20), primary_key=True)
    download_id = Column(String(36, 'utf8mb4_unicode_520_ci'), nullable=False)
    product_id = Column(BIGINT(20), nullable=False)
    order_id = Column(BIGINT(20), nullable=False, index=True, server_default=text("'0'"))
    order_key = Column(String(200, 'utf8mb4_unicode_520_ci'), nullable=False)
    user_email = Column(String(200, 'utf8mb4_unicode_520_ci'), nullable=False)
    user_id = Column(BIGINT(20))
    downloads_remaining = Column(String(9, 'utf8mb4_unicode_520_ci'))
    access_granted = Column(DateTime, nullable=False, server_default=text("'0000-00-00 00:00:00'"))
    access_expires = Column(DateTime)
    download_count = Column(BIGINT(20), nullable=False, server_default=text("'0'"))


class WpWoocommerceLog(Base):
    __tablename__ = 'wp_woocommerce_log'

    log_id = Column(BIGINT(20), primary_key=True)
    timestamp = Column(DateTime, nullable=False)
    level = Column(SMALLINT(4), nullable=False, index=True)
    source = Column(String(200, 'utf8mb4_unicode_520_ci'), nullable=False)
    message = Column(LONGTEXT, nullable=False)
    context = Column(LONGTEXT)


class WpWoocommerceOrderItemmeta(Base):
    __tablename__ = 'wp_woocommerce_order_itemmeta'

    meta_id = Column(BIGINT(20), primary_key=True)
    order_item_id = Column(BIGINT(20), nullable=False, index=True)
    meta_key = Column(String(255, 'utf8mb4_unicode_520_ci'), index=True)
    meta_value = Column(LONGTEXT)


class WpWoocommerceOrderItem(Base):
    __tablename__ = 'wp_woocommerce_order_items'

    order_item_id = Column(BIGINT(20), primary_key=True)
    order_item_name = Column(Text(collation='utf8mb4_unicode_520_ci'), nullable=False)
    order_item_type = Column(String(200, 'utf8mb4_unicode_520_ci'), nullable=False, server_default=text("''"))
    order_id = Column(BIGINT(20), nullable=False, index=True)


class WpWoocommercePaymentTokenmeta(Base):
    __tablename__ = 'wp_woocommerce_payment_tokenmeta'

    meta_id = Column(BIGINT(20), primary_key=True)
    payment_token_id = Column(BIGINT(20), nullable=False, index=True)
    meta_key = Column(String(255, 'utf8mb4_unicode_520_ci'), index=True)
    meta_value = Column(LONGTEXT)


class WpWoocommercePaymentToken(Base):
    __tablename__ = 'wp_woocommerce_payment_tokens'

    token_id = Column(BIGINT(20), primary_key=True)
    gateway_id = Column(String(200, 'utf8mb4_unicode_520_ci'), nullable=False)
    token = Column(Text(collation='utf8mb4_unicode_520_ci'), nullable=False)
    user_id = Column(BIGINT(20), nullable=False, index=True, server_default=text("'0'"))
    type = Column(String(200, 'utf8mb4_unicode_520_ci'), nullable=False)
    is_default = Column(TINYINT(1), nullable=False, server_default=text("'0'"))


class WpWoocommerceSession(Base):
    __tablename__ = 'wp_woocommerce_sessions'

    session_id = Column(BIGINT(20), primary_key=True)
    session_key = Column(CHAR(32, 'utf8mb4_unicode_520_ci'), nullable=False, unique=True)
    session_value = Column(LONGTEXT, nullable=False)
    session_expiry = Column(BIGINT(20), nullable=False)


class WpWoocommerceShippingZoneLocation(Base):
    __tablename__ = 'wp_woocommerce_shipping_zone_locations'
    __table_args__ = (
        Index('location_type_code', 'location_type', 'location_code'),
    )

    location_id = Column(BIGINT(20), primary_key=True, index=True)
    zone_id = Column(BIGINT(20), nullable=False)
    location_code = Column(String(200, 'utf8mb4_unicode_520_ci'), nullable=False)
    location_type = Column(String(40, 'utf8mb4_unicode_520_ci'), nullable=False)


class WpWoocommerceShippingZoneMethod(Base):
    __tablename__ = 'wp_woocommerce_shipping_zone_methods'

    zone_id = Column(BIGINT(20), nullable=False)
    instance_id = Column(BIGINT(20), primary_key=True)
    method_id = Column(String(200, 'utf8mb4_unicode_520_ci'), nullable=False)
    method_order = Column(BIGINT(20), nullable=False)
    is_enabled = Column(TINYINT(1), nullable=False, server_default=text("'1'"))


class WpWoocommerceShippingZone(Base):
    __tablename__ = 'wp_woocommerce_shipping_zones'

    zone_id = Column(BIGINT(20), primary_key=True)
    zone_name = Column(String(200, 'utf8mb4_unicode_520_ci'), nullable=False)
    zone_order = Column(BIGINT(20), nullable=False)


class WpWoocommerceTaxRateLocation(Base):
    __tablename__ = 'wp_woocommerce_tax_rate_locations'
    __table_args__ = (
        Index('location_type_code', 'location_type', 'location_code'),
    )

    location_id = Column(BIGINT(20), primary_key=True)
    location_code = Column(String(200, 'utf8mb4_unicode_520_ci'), nullable=False)
    tax_rate_id = Column(BIGINT(20), nullable=False, index=True)
    location_type = Column(String(40, 'utf8mb4_unicode_520_ci'), nullable=False)


class WpWoocommerceTaxRate(Base):
    __tablename__ = 'wp_woocommerce_tax_rates'

    tax_rate_id = Column(BIGINT(20), primary_key=True)
    tax_rate_country = Column(String(2, 'utf8mb4_unicode_520_ci'), nullable=False, index=True, server_default=text("''"))
    tax_rate_state = Column(String(200, 'utf8mb4_unicode_520_ci'), nullable=False, index=True, server_default=text("''"))
    tax_rate = Column(String(8, 'utf8mb4_unicode_520_ci'), nullable=False, server_default=text("''"))
    tax_rate_name = Column(String(200, 'utf8mb4_unicode_520_ci'), nullable=False, server_default=text("''"))
    tax_rate_priority = Column(BIGINT(20), nullable=False, index=True)
    tax_rate_compound = Column(INTEGER(1), nullable=False, server_default=text("'0'"))
    tax_rate_shipping = Column(INTEGER(1), nullable=False, server_default=text("'1'"))
    tax_rate_order = Column(BIGINT(20), nullable=False)
    tax_rate_class = Column(String(200, 'utf8mb4_unicode_520_ci'), nullable=False, index=True, server_default=text("''"))


class WpWpfFilter(Base):
    __tablename__ = 'wp_wpf_filters'

    id = Column(INTEGER(11), primary_key=True)
    title = Column(String(128))
    setting_data = Column(Text, nullable=False)


class WpWpfModule(Base):
    __tablename__ = 'wp_wpf_modules'

    id = Column(SMALLINT(3), primary_key=True)
    code = Column(String(32), nullable=False, unique=True)
    active = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
    type_id = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
    label = Column(String(64))
    ex_plug_dir = Column(String(255))


class WpWpfModulesType(Base):
    __tablename__ = 'wp_wpf_modules_type'

    id = Column(SMALLINT(3), primary_key=True)
    label = Column(String(32), nullable=False)


class WpWpfUsageStat(Base):
    __tablename__ = 'wp_wpf_usage_stat'

    id = Column(INTEGER(11), primary_key=True)
    code = Column(String(64), nullable=False, unique=True)
    visits = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    spent_time = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    modify_timestamp = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))


class WpWcDownloadLog(Base):
    __tablename__ = 'wp_wc_download_log'

    download_log_id = Column(BIGINT(20), primary_key=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    permission_id = Column(ForeignKey('wp_woocommerce_downloadable_product_permissions.permission_id', ondelete='CASCADE'), nullable=False, index=True)
    user_id = Column(BIGINT(20))
    user_ip_address = Column(String(100, 'utf8mb4_unicode_520_ci'), server_default=text("''"))

    permission = relationship('WpWoocommerceDownloadableProductPermission')
